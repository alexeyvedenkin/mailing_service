from typing import Any

from .models import NewsLetter, SendingAttempt, Recipient


class NewsletterService:

    @classmethod
    def overall_statistics(cls) -> Any:
        """Получение общей статистики по всем рассылкам"""
        try:
            total_newsletters = NewsLetter.objects.count()  # Общее количество рассылок
            active_count = NewsLetter.active_count()
            total_attempts = SendingAttempt.objects.count()  # Общее количество попыток
            successful_attempts = SendingAttempt.objects.filter(status="success").count()  # Успешные попытки
            failed_attempts = SendingAttempt.objects.filter(status="failure").count()  # Неудачные попытки
            unique_recipient_count = NewsLetter.unique_recipient_count()

            return {
                "total_newsletters": total_newsletters,
                "active_count": active_count,
                "total_attempts": total_attempts,
                "successful_attempts": successful_attempts,
                "failed_attempts": failed_attempts,
                "unique_recipient_count": unique_recipient_count,
            }
        except Exception as e:
            print(f"Ошибка: {e}")  # Выводим ошибку в консоль
            return {  # Возвращаем пустые значения вместо None
                "total_newsletters": 0,
                "active_count": 0,
                "total_attempts": 0,
                "successful_attempts": 0,
                "failed_attempts": 0,
                "unique_recipient_count": 0,
            }

    @staticmethod
    def get_newsletter_info(self) -> Any:
        """Получение информации о состоянии всех полей рассылки"""
        # Формируем информацию о рассылке

        # Получаем всех получателей
        recipients_list = self.recipients.all()  # Изменено: получаем список всех получателей

        info = {
            "owner": self.owner.id,
            "first_send_time": self.first_send_time,
            "last_send_time": self.last_send_time,
            "status": self.get_status_display(),  # Используем метод для отображения статуса
            "message": self.message.content,  # Содержимое сообщения
            "recipients_count": len(recipients_list),  # Теперь используем количество получателей из списка
            "recipients_emails": [recipient.email for recipient in recipients_list],  # Получаем emails
        }

        # Вывод информации на консоль
        print("Информация о рассылке:")
        for key, value in info.items():
            print(f"{key}: {value}")  # Выводим ключ и его значение

        return info  # Возвращаем информацию о рассылке
