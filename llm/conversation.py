from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from langgraph.checkpoint.memory import InMemorySaver

MAX_MESSAGES = 100

INACTIVITY_TIMEOUT = timedelta(
    minutes=30,
)

@dataclass
class ConversationMetadata:
    generation: int
    message_count: int
    last_activity: datetime

class ConversationManager:
    def __init__(
        self,
        checkpointer: InMemorySaver,
    ) -> None:

        self.checkpointer = checkpointer

        self._conversations: dict[
            str,
            ConversationMetadata,
        ] = {}

    @staticmethod
    def _now() -> datetime:
        """
        Return the current time in UTC.
        """

        return datetime.now(
            timezone.utc,
        )

    @staticmethod
    def _conversation_key(
        user_id: str,
        project_id: str,
    ) -> str:
        return f"{user_id}:{project_id}"

    def _get_or_create(
        self,
        user_id: str,
        project_id: str,
    ) -> ConversationMetadata:
        key = self._conversation_key(
            user_id,
            project_id,
        )

        metadata = self._conversations.get(
            key,
        )

        if metadata is not None:
            return metadata

        metadata = ConversationMetadata(
            generation=1,
            message_count=0,
            last_activity=self._now(),
        )

        self._conversations[key] = metadata

        return metadata

    @staticmethod
    def _thread_id(
        user_id: str,
        project_id: str,
        generation: int,
    ) -> str:
        return (
            f"user:{user_id}:project:{project_id}:{generation}"
        )

    def current_thread_id(
        self,
        user_id: str,
        project_id: str,
    ) -> str:
        metadata = self._get_or_create(
            user_id,
            project_id,
        )

        return self._thread_id(
            user_id=user_id,
            project_id=project_id,
            generation=metadata.generation,
        )

    def _is_expired(
        self,
        metadata: ConversationMetadata,
    ) -> bool:
        if metadata.message_count >= MAX_MESSAGES:
            return True

        inactive_for = (
            self._now()
            - metadata.last_activity
        )

        if inactive_for >= INACTIVITY_TIMEOUT:
            return True

        return False

    def _delete_thread(
        self,
        thread_id: str,
    ) -> None:
        self.checkpointer.delete_thread(
            thread_id,
        )

    def prepare(
        self,
        user_id: str,
        project_id: str,
    ) -> str:
        metadata = self._get_or_create(
            user_id,
            project_id,
        )
        if self._is_expired(
            metadata,
        ):

            old_thread_id = self._thread_id(
                user_id=user_id,
                project_id=project_id,
                generation=metadata.generation,
            )

            self._delete_thread(
                old_thread_id,
            )

            key = self._conversation_key(
                user_id,
                project_id,
            )

            metadata = ConversationMetadata(
                generation=metadata.generation + 1,
                message_count=0,
                last_activity=self._now(),
            )

            self._conversations[key] = metadata

        return self._thread_id(
            user_id=user_id,
            project_id=project_id,
            generation=metadata.generation,
        )

    def record_message(
        self,
        user_id: str,
        project_id: str,
    ) -> None:
        metadata = self._get_or_create(
            user_id,
            project_id,
        )

        metadata.message_count += 1

        metadata.last_activity = self._now()
