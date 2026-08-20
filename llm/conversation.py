from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from langgraph.checkpoint.memory import InMemorySaver


# =============================================================================
# CONVERSATION LIMITS
# =============================================================================

MAX_MESSAGES = 100

INACTIVITY_TIMEOUT = timedelta(
    minutes=30,
)


# =============================================================================
# CONVERSATION METADATA
# =============================================================================

@dataclass
class ConversationMetadata:
    """
    Metadata about a user's current conversation.

    This does NOT contain conversation messages.

    LangGraph's checkpointer stores the actual conversation state.
    """

    generation: int

    message_count: int

    last_activity: datetime


# =============================================================================
# CONVERSATION MANAGER
# =============================================================================

class ConversationManager:
    """
    Manages the lifecycle of temporary LangGraph conversations.
    """

    def __init__(
        self,
        checkpointer: InMemorySaver,
    ) -> None:

        self.checkpointer = checkpointer

        self._conversations: dict[
            str,
            ConversationMetadata,
        ] = {}

    # =========================================================================
    # CURRENT TIME
    # =========================================================================

    @staticmethod
    def _now() -> datetime:
        """
        Return the current time in UTC.
        """

        return datetime.now(
            timezone.utc,
        )

    # =========================================================================
    # GET OR CREATE METADATA
    # =========================================================================

    def _get_or_create(
        self,
        user_id: str,
    ) -> ConversationMetadata:
        """
        Get the current conversation metadata.

        Creates generation 1 when the user has no conversation yet.
        """

        metadata = self._conversations.get(
            user_id,
        )

        if metadata is not None:
            return metadata

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

            user:123:1
        """

        return (
            f"user:{user_id}:{generation}"
        )

    # =========================================================================
    # CURRENT THREAD ID
    # =========================================================================

    def current_thread_id(
        self,
        user_id: str,
    ) -> str:
        """
        Return the user's current thread ID.

        This does NOT create a new generation.

        If the user has never had a conversation, generation 1 is created.
        """

        metadata = self._get_or_create(
            user_id,
        )

        return self._thread_id(
            user_id=user_id,
            generation=metadata.generation,
        )

    # =========================================================================
    # CHECK EXPIRATION
    # =========================================================================

    def _is_expired(
        self,
        metadata: ConversationMetadata,
    ) -> bool:
        """
        Determine whether the current conversation has expired.
        """

        # ---------------------------------------------------------------------
        # MESSAGE LIMIT
        # ---------------------------------------------------------------------

        if metadata.message_count >= MAX_MESSAGES:
            return True

        # ---------------------------------------------------------------------
        # INACTIVITY LIMIT
        # ---------------------------------------------------------------------

        inactive_for = (
            self._now()
            - metadata.last_activity
        )

        if inactive_for >= INACTIVITY_TIMEOUT:
            return True

        return False

    # =========================================================================
    # DELETE THREAD
    # =========================================================================

    def _delete_thread(
        self,
        thread_id: str,
    ) -> None:
        """
        Delete a LangGraph conversation.
        """

        self.checkpointer.delete_thread(
            thread_id,
        )

    # =========================================================================
    # PREPARE
    # =========================================================================

    def prepare(
        self,
        user_id: str,
    ) -> str:
        """
        Prepare the conversation before processing a new user message.
        """

        metadata = self._get_or_create(
            user_id,
        )

        # ---------------------------------------------------------------------
        # CHECK EXPIRATION
        # ---------------------------------------------------------------------

        if self._is_expired(
            metadata,
        ):

            old_thread_id = self._thread_id(
                user_id=user_id,
                generation=metadata.generation,
            )

            # -----------------------------------------------------------------
            # DELETE OLD LANGGRAPH THREAD
            # -----------------------------------------------------------------

            self._delete_thread(
                old_thread_id,
            )

            # -----------------------------------------------------------------
            # CREATE NEW GENERATION
            # -----------------------------------------------------------------

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

        metadata = self._get_or_create(
            user_id,
        )

        metadata.message_count += 1

        metadata.last_activity = self._now()