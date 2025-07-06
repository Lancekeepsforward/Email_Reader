class EmailSample:
    def __init__(
        self,
        id: str = "",
        thread_id: str = "",
        subject: str = "",
        sender: str = "",
        receiver: str = "",
        date: str = "",
        content: str = "",
        word_count: int = None,
        sentence_count: int = None,
    ):
        self.id = id
        self.thread_id = thread_id
        self.subject = subject
        self.sender = sender
        self.receiver = receiver
        self.date = date
        self.content = content
        if (word_count is None or sentence_count is None) and len(content) > 0:
            self.word_count, self.sentence_count = self.content_stats()
        else:
            self.word_count = word_count
            self.sentence_count = sentence_count

    def __str__(self):
        return f"【Id】: {self.id}\n【Thread ID】: {self.thread_id}\n【Subject】: {self.subject}\n【Sender】: {self.sender}\n【Receiver】: {self.receiver}\n【Date】: {self.date}\n【Content】: {self.content}\n【Word Count】: {self.word_count}\n【Sentence Count】: {self.sentence_count}"

    def __repr__(self):
        return f"EmailSample(id={self.id}, thread_id={self.thread_id}, subject={self.subject}, sender={self.sender}, receiver={self.receiver}, date={self.date}, content={self.content}, word_count={self.word_count}, sentence_count={self.sentence_count})"
    
    def __eq__(self, other):
        return self.id == other.id and self.thread_id == other.thread_id

    def set_content(self, content: str):
        self.content = content
        self.word_count, self.sentence_count = self.content_stats()

    def set_subject(self, subject: str):
        self.subject = subject

    def set_sender(self, sender: str):
        self.sender = sender

    def set_receiver(self, receiver: str):
        self.receiver = receiver

    def set_date(self, date: str):
        self.date = date

    def get_content(self):
        return self.content

    def get_subject(self):
        return self.subject

    def get_sender(self):
        return self.sender

    def get_receiver(self):
        return self.receiver

    def get_date(self):
        return self.date

    def get_id(self):
        return self.id

    def get_thread_id(self):
        return self.thread_id

    def content_stats(self):
        if len(self.content) == 0:
            return 0, 0
        word_count = len(self.content.split())
        sentence_count = (
            len(self.content.split(".")) + len(self.content.split("\n"))
        ) // 2
        return word_count, sentence_count
