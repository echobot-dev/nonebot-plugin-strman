from typing import Iterable, Mapping, Type, Union

from nonebot.adapters import Message, MessageSegment


def make_fake_message():
    from nonebot.adapters import Message, MessageSegment

    class FakeMessageSegment(MessageSegment):
        @classmethod
        def get_message_class(cls):
            return FakeMessage

        def __str__(self) -> str:
            return self.data["text"] if self.type == "text" else f"[fake:{self.type}]"

        @classmethod
        def text(cls, text: str):
            return cls("text", {"text": text})

        @staticmethod
        def image(url: str):
            return FakeMessageSegment("image", {"url": url})

        @classmethod
        def face(cls, id: int):
            return cls("face", {"id": id})

        def is_text(self) -> bool:
            return self.type == "text"

    class FakeMessage(Message):
        @classmethod
        def get_segment_class(cls):
            return FakeMessageSegment

        @staticmethod
        def _construct(msg: Union[str, Iterable[Mapping]]):
            if isinstance(msg, str):
                yield FakeMessageSegment.text(msg)
            else:
                for seg in msg:
                    yield FakeMessageSegment(**seg)

        def __add__(self, other):
            return super().__add__(other)

    return FakeMessage
