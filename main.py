from first_agent import ProfileCollectorAgent, model

agent1 = ProfileCollectorAgent(model)

user_text = """
Hello, my name is Rohan Singh. My CGPA is 8.3. I want to become a software engineer at a product-based company.

My technical skills include: Python, Java, SQL, DSA, Git, and basic system design.

I have solved around 280 DSA problems on LeetCode and GFG combined. My competitive programming rating is around 1450 on CodeChef.

Projects I have built:
1. Student Management System using Java and SQL
2. News Summarizer using Python and NLP
3. Personal Portfolio Website

I have done 1 internship as a backend developer at a startup.

"""

profile = agent1.collect(user_text)
print(profile)

from second_agent import ReadinessEvaluatorAgent

agent2 = ReadinessEvaluatorAgent()

evaluation= agent2.evaluate(profile=profile)

print(evaluation)


from third_agent import GapDetectorAgent

agent3 = GapDetectorAgent()

gap = agent3.find_gap(profile=profile,evaluation=evaluation)

print(gap)

from fourth_agent import RoadmapAgent

agent4 = RoadmapAgent()

roadmap = agent4.generate_roadmap(
    profile=profile,
    evaluation=evaluation,
    gaps=gap
)

print("\nFINAL 7-DAY ROADMAP:\n", roadmap)
