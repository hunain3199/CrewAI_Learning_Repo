
from crewai.flow.flow import Flow, start, listen, router
from litellm import completion
import os

os.environ['GEMINI_API_KEY'] = "AIzaSyAo_vo4SvEnXktWQfO-hcqbUNZLGvTZiJE"


class RoutedFlow(Flow):
    model = "gemini/gemini-2.0-flash-exp"

    @start()
    def generate_topic(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Generate a blog topic for 2025."}]
        )
        topic = response["choices"][0]["message"]["content"].strip()
        # For demonstration, add a fake flag to the state.
        self.state["is_tech"] = "tech" in topic.lower()
        print(f"Topic: {topic}")
        return topic

    @router(generate_topic)
    def route_topic(self):
        # Route based on the is_tech flag.
        if self.state.get("is_tech"):
            return "tech_route"
        else:
            return "lifestyle_route"

    @listen("tech_route")
    def generate_tech_outline(self, topic):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Create a detailed tech blog outline for: {topic}"}]
        )
        outline = response["choices"][0]["message"]["content"].strip()
        print("Tech Outline:")
        print(outline)
        return outline

    @listen("lifestyle_route")
    def generate_lifestyle_outline(self, topic):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Create a detailed lifestyle blog outline for: {topic}"}]
        )
        outline = response["choices"][0]["message"]["content"].strip()
        print("Lifestyle Outline:")
        print(outline)
        return outline


def main():
    flow = RoutedFlow()
    flow.plot()
    final_output = flow.kickoff()
    print("Final Output:")
    print(final_output)


if __name__ == "__main__":
    main()