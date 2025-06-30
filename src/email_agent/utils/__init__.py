# 只导入没有外部依赖的模块
from .email_sample import EmailSample
from .email_fetcher import main as fetch_save_emails, save_emails_id_threading
from .email_parser import get_email_content_list, modify_content, main as get_email_samples
from .credential import main as get_creds

# 定义包的公共接口
__all__ = [
    "EmailSample",
    "fetch_save_emails",
    "save_emails_id_threading",
    "get_email_content_list",
    "modify_content",
    "get_creds",
    "get_email_samples"
]

if __name__ == "__main__":
    pass