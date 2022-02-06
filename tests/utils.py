from nonebot.adapters import Message, MessageSegment


class FakeMessageSegment(MessageSegment):

    @classmethod
    def get_message_class(cls):
        return FakeMessage

    def __str__(self) -> str:
        return (self.data['text']
                if self.type == 'text' else f'[fake:{self.type}]')

    @classmethod
    def text(cls, text: str):
        return cls('text', {'text': text})

    @classmethod
    def image(cls, url: str):
        return cls('image', {'url': url})

    @classmethod
    def face(cls, id: int):
        return cls('face', {'id': id})

    def is_text(self) -> bool:
        return self.type == 'text'


class FakeMessage(Message):

    @classmethod
    def get_segment_class(cls):
        return FakeMessageSegment

    @staticmethod
    def _construct(msg: str):
        yield FakeMessageSegment.text(msg)
