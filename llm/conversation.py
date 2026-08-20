from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from langgraph.checkpoint.memory import InMemorySaver


# =============================================================================
# CONVERSATION LIMITS
# =============================================================================

# Maximum number of USER messages allowed in one conversation.
MAX_MESSAGES = 100

# Conversation expires after 30 minutes without user activity.
INACTIVITY_TIMEOUT = timedelta(minutes=30)


# =============================================================================
# CONVERSATION METADATA
# =============================================================================


@dataclass
class ConversationMetadata:
    """
    Small amount of metadata about a user's current conversation.

    IMPORTANT:
    This does NOT contain the actual conversation history.

    The actual history is stored by LangGraph's checkpointer.
    """

    # Conversation generation.

    # Example:
    #
    # user:123:1
    # user:123:2
    # user:123:3
    #
    # Every generation represents a different conversation.

    generation: int

    # Number of user messages in this conversation.
    message_count: int

    # When the user last sent a message.
    last_activity: datetime


# =============================================================================
# CONVERSATION MANAGER
# =============================================================================


class ConversationManager:
    """
    Manages the lifecycle of temporary conversations.

    Responsibilities:

    - Track message count.
    - Track last activity.
    - Detect 100-message limit.
    - Detect 30-minute inactivity.
    - Delete expired LangGraph conversations.
    - Create new conversation generations.

    This metadata itself lives in server RAM.
    """

    def __init__(
        self,
        checkpointer: InMemorySaver,
    ) -> None:
        """
        Create a conversation manager.

        We receive the same checkpointer that the LangGraph agent uses.

        This is important because when a conversation expires we need to
        delete the corresponding thread from that exact checkpointer.
        """

        self.checkpointer = checkpointer

        self._conversations: dict[str, ConversationMetadata] = {}


    # =========================================================================
    # CURRENT TIME
    # =========================================================================

    @staticmethod
    def _now() -> datetime:
        """
        Return the current time in UTC.
        """

        return datetime.now(timezone.utc)


    # =========================================================================
    # GET OR CREATE METADATA
    # =========================================================================

    def _get_or_create(
        self,
        user_id: str,
    ) -> ConversationMetadata:
        """
        Get the user's current conversation metadata.

        If the user has never started a conversation, create generation 1.
        """

        metadata = self._conversations.get(user_id)

        if metadata is not None:
            return metadata


        # ---------------------------------------------------------------------
        # FIRST CONVERSATION FOR THIS USER
        # ---------------------------------------------------------------------

        metadata = ConversationMetadata(
            generation=1,
            message_count=0,
            last_activity=self._now(),
        )

        self._conversations[user_id] = metadata

        return metadata


    # =========================================================================
    # BUILD THREAD ID
    # =========================================================================

    @staticmethod
    def _thread_id(
        user_id: str,
        generation: int,
    ) -> str:
        """
        Build the LangGraph thread ID.

        Example:

            user_id = 123
            generation = 2

            result:
                user:123:2
        """

        return f"user:{user_id}:{generation}"


    # =========================================================================
    # CHECK EXPIRATION
    # =========================================================================

    def _is_expired(
        self,
        metadata: ConversationMetadata,
    ) -> bool:
        """
        Determine whether the conversation has expired.
        """

        # ---------------------------------------------------------------------
        # MESSAGE LIMIT
        # ---------------------------------------------------------------------

        if metadata.message_count >= MAX_MESSAGES:
            return True


        # ---------------------------------------------------------------------
        # INACTIVITY LIMIT
        # ---------------------------------------------------------------------

        inactive_for = self._now() - metadata.last_activity

        if inactive_for >= INACTIVITY_TIMEOUT:
            return True


        return False


    # =========================================================================
    # DELETE EXPIRED CONVERSATION
    # =========================================================================

    def _delete_thread(
        self,
        thread_id: str,
    ) -> None:
        """
        Permanently remove the conversation from LangGraph's checkpointer.

        InMemorySaver provides a public delete_thread() method, so we use
        that instead of touching its internal storage dictionary.
        """

        self.checkpointer.delete_thread(thread_id)


    # =========================================================================
    # PREPARE CONVERSATION
    # =========================================================================

    def prepare(
        self,
        user_id: str,
    ) -> str:
        """
        Prepare the conversation before processing a new message.

        This method:

        1. Gets the current conversation.
        2. Checks whether it expired.
        3. Deletes the old LangGraph thread if necessary.
        4. Creates a new generation if necessary.
        5. Returns the thread ID to use.
        """

        metadata = self._get_or_create(user_id)


        # ---------------------------------------------------------------------
        # CHECK WHETHER CURRENT CONVERSATION HAS EXPIRED
        # ---------------------------------------------------------------------

        if self._is_expired(metadata):

            # ---------------------------------------------------------------
            # BUILD OLD THREAD ID
            # ---------------------------------------------------------------

            old_thread_id = self._thread_id(
                user_id=user_id,
                generation=metadata.generation,
            )


            # ---------------------------------------------------------------
            # ACTUALLY DELETE OLD CONVERSATION
            # ---------------------------------------------------------------
            #
            # This removes the old checkpoint state from InMemorySaver.
            #
            # So we're not merely ignoring:
            #
            #     user:123:1
            #
            # We actually delete it.
            # ---------------------------------------------------------------

            self._delete_thread(old_thread_id)


            # ---------------------------------------------------------------
            # CREATE NEW GENERATION
            # ---------------------------------------------------------------

            metadata = ConversationMetadata(
                generation=metadata.generation + 1,
                message_count=0,
                last_activity=self._now(),
            )

            self._conversations[user_id] = metadata


        # ---------------------------------------------------------------------
        # RETURN CURRENT THREAD
        # ---------------------------------------------------------------------

        return self._thread_id(
            user_id=user_id,
            generation=metadata.generation,
        )


    # =========================================================================
    # RECORD MESSAGE
    # =========================================================================

    def record_message(
        self,
        user_id: str,
    ) -> None:
        """
        Record one successfully processed user message.
        """

        metadata = self._get_or_create(user_id)

        metadata.message_count += 1

        metadata.last_activity = self._now()