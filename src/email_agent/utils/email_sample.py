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
    ):
        self.id = id
        self.thread_id = thread_id
        self.subject = subject
        self.sender = sender
        self.receiver = receiver
        self.date = date
        self.content = content
        self.word_count, self.sentence_count = self.content_stats()

    def __str__(self):
        if self.sentence_count < 30:
            return f"Id: {self.id}\nThread ID: {self.thread_id}\nSubject: {self.subject}\nSender: {self.sender}\nReceiver: {self.receiver}\nDate: {self.date}\nContent: {self.content}\nWord Count: {self.word_count}\nSentence Count: {self.sentence_count}"
        else:
            return f"Id: {self.id}\nThread ID: {self.thread_id}\nSubject: {self.subject}\nSender: {self.sender}\nReceiver: {self.receiver}\nDate: {self.date}\nContent: {self.content[:500]}...\nWord Count: {self.word_count}\nSentence Count: {self.sentence_count}"

    def __repr__(self):
        return f"EmailSample(id={self.id}, thread_id={self.thread_id}, subject={self.subject}, sender={self.sender}, receiver={self.receiver}, date={self.date}, content={self.content})"

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
        word_count = len(self.content.split())
        sentence_count = (
            len(self.content.split(".")) + len(self.content.split("\n"))
        ) // 2
        return word_count, sentence_count
