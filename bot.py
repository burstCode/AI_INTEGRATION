from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential


class Bot:
    """
    Класс бота, инициализирует нужные переменные для подключения
    к github models и реализует методы для отправки запросов к моделям
    """

    _model_name: str
    _client: ChatCompletionsClient

    def __init__(self, endpoint: str, token: str, model_name: str) -> None:
        """

        :param endpoint: Адрес ai.azure
        :param token: Сгенерированный токен на github
        :param model_name: Имя модели
        """

        self._client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )

        self._model_name = model_name

    def send_request(self, prompt: str) -> str:
        """
        Отправка запроса нейросети
        :param prompt: Запрос пользователя на естественном языке
        :return: Ответ нейросети
        """

        response = self._client.complete(
            messages=[
                UserMessage(prompt),
            ],
            max_tokens=1000,
            model=self._model_name
        )

        return response.choices[0].message.content
