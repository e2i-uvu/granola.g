import os

from openai import OpenAI
import tiktoken


class GPT:

    def __init__(
        self,
        openai_api_key: str | None = os.environ.get("OPENAI_API_KEY"),
        model: str = "gpt-4o",
        sys_msg: str = "You are a helpful assistant",
        temp: float = 0.5,
        name: str = "",
        messages: list = [],
        moderation_model: str = "text-moderation-latest",
    ):
        self.openai_api_key = openai_api_key
        self.model = model
        self.sys_msg = self.add_msg(role="system", content=sys_msg)
        self.temp = temp
        self.name = name
        self.messages = messages
        self.moderation_model = moderation_model

        self.context_length = {
            "gpt-4o": 128_000,
            "gpt-4o-mini": 128_000,
            "gpt-4-turbo": 128_000,
            "gpt-4-turbo-2024-04-09": 128_000,
            "gpt-4-turbo-preview": 128_000,
            "gpt-4-0125-preview": 128_000,
            "gpt-4-1106-preview": 128_000,
            "gpt-4-vision-preview": 128_000,
            "gpt-4-1106-vision-preview": 128_000,
            "gpt-4": 8_192,
            "gpt-4-0613": 8_192,
            "gpt-4-32k": 32_768,
            "gpt-4-32k-0613": 32_768,
            "gpt-3.5-turbo-0125": 16_385,
            "gpt-3.5-turbo": 16_385,
            "gpt-3.5-turbo-1106": 16_385,
            "gpt-3.5-turbo-instruct": 4_096,
            "gpt-3.5-turbo-16k": 16_385,
            "gpt-3.5-turbo-0613": 4_096,
            "gpt-3.5-turbo-16k-0613": 16_385,
        }

        if self.openai_api_key is None:
            raise AssertionError("`OPENAI_API_KEY` not set")
        else:
            self.client = OpenAI(api_key=self.openai_api_key)

        try:
            self.encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def add_msg(
        self,
        role: str,
        content: str,
        name: str = "",
        tool_calls: list = [],
        tool_call_id: str = "",
    ) -> None:

        if role == "system" or role == "user":
            if name:
                self.messages.append({"role": role, "content": content, "name": name})
            else:
                self.messages.append({"role": role, "content": content})

        elif role == "assistant":
            if name and tool_calls:
                self.messages.append(
                    {
                        "role": role,
                        "content": content,
                        "name": name,
                        "tool_calls": tool_calls,
                    }
                )

            if name and not tool_calls:
                self.messages.append(
                    {
                        "role": role,
                        "content": content,
                        "name": name,
                    }
                )

            if not name and tool_calls:
                self.messages.append(
                    {
                        "role": role,
                        "content": content,
                        "tool_calls": tool_calls,
                    }
                )

            else:
                self.messages.append({"role": role, "content": content})

        elif role == "tool":
            if not tool_call_id:
                raise AssertionError("`tool_call_id` is required")

            self.messages.append(
                {"role": role, "content": content, "tool_call_id": tool_call_id}
            )

    def moderate(self, query: str) -> bool:
        """
        Check for inappropriate messages before sending to OpenAI.
        Returns True if `query` is flagged as inappropriate
        """
        mod = self.client.moderations.create(input=query)

        # log results if flagged
        for r in mod.results:
            if r.flagged:
                # logging here
                return True

        return False

    def run(self):
        pass

    def tools(self, query: str):
        """Model can use 'tools'"""
        if query:
            if self.moderate(query):
                pass  # TODO:

            self.add_msg(role="user", content=query, name=self.name)

    def stream(self):
        pass


if __name__ == "__main__":
    gpt = GPT()
