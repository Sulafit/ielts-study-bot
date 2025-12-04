"""
IELTS 30-Day Topic-Related Vocabulary Plan
Each day has a specific topic with key vocabulary and phrases
"""

from datetime import datetime, date
from typing import Dict, Tuple

# 30-day IELTS vocabulary plan
# Format: day_number: (topic_name, category, key_vocabulary)
TOPICS_PLAN = {
    # WEEK 1 – Personal Topics
    1: {
        "name": "Family",
        "category": "Personal Topics",
        "week": 1,
        "key_areas": [
            "Family relationships and structures",
            "Describing family members",
            "Family activities and traditions",
            "Modern family issues"
        ],
        "vocabulary": [
            "nuclear family",
            "extended family",
            "single-parent family",
            "close-knit family",
            "family bond",
            "blood relative",
            "breadwinner",
            "upbringing",
            "generation gap",
            "family values"
        ]
    },
    2: {
        "name": "Education",
        "category": "Personal Topics",
        "week": 1,
        "key_areas": [
            "Education systems",
            "Learning methods",
            "Academic achievement",
            "Educational institutions"
        ],
        "vocabulary": [
            "compulsory education",
            "curriculum",
            "academic performance",
            "distance learning",
            "hands-on experience",
            "practical skills",
            "theoretical knowledge",
            "lifelong learning",
            "critical thinking",
            "educational attainment"
        ]
    },
    3: {
        "name": "Work / Career",
        "category": "Personal Topics",
        "week": 1,
        "key_areas": [
            "Job types and sectors",
            "Career development",
            "Work-life balance",
            "Employment challenges"
        ],
        "vocabulary": [
            "career prospects",
            "job satisfaction",
            "work-life balance",
            "professional development",
            "job security",
            "competitive salary",
            "career advancement",
            "flexible working hours",
            "job market",
            "unemployment rate"
        ]
    },
    4: {
        "name": "Hobbies / Leisure",
        "category": "Personal Topics",
        "week": 1,
        "key_areas": [
            "Types of hobbies",
            "Benefits of leisure activities",
            "Indoor and outdoor activities",
            "Free time management"
        ],
        "vocabulary": [
            "leisure activities",
            "recreational pursuits",
            "spare time",
            "pastime",
            "physical exercise",
            "mental stimulation",
            "stress relief",
            "social interaction",
            "creative outlet",
            "time-consuming"
        ]
    },
    5: {
        "name": "Food",
        "category": "Personal Topics",
        "week": 1,
        "key_areas": [
            "Food preferences and diet",
            "Cooking and eating habits",
            "Food culture",
            "Health and nutrition"
        ],
        "vocabulary": [
            "balanced diet",
            "nutritious food",
            "processed food",
            "organic produce",
            "eating habits",
            "culinary traditions",
            "fast food",
            "home-cooked meals",
            "food security",
            "dietary requirements"
        ]
    },
    6: {
        "name": "Health",
        "category": "Personal Topics",
        "week": 1,
        "key_areas": [
            "Physical and mental health",
            "Healthcare systems",
            "Healthy lifestyle",
            "Common health issues"
        ],
        "vocabulary": [
            "physical fitness",
            "mental well-being",
            "preventive care",
            "medical treatment",
            "healthcare system",
            "healthy lifestyle",
            "sedentary lifestyle",
            "chronic disease",
            "life expectancy",
            "health insurance"
        ]
    },
    7: {
        "name": "Technology",
        "category": "Personal Topics",
        "week": 1,
        "key_areas": [
            "Modern technology",
            "Digital devices",
            "Impact on daily life",
            "Technology in communication"
        ],
        "vocabulary": [
            "technological advancement",
            "digital revolution",
            "cutting-edge technology",
            "user-friendly",
            "online platform",
            "social media",
            "instant communication",
            "digital literacy",
            "tech-savvy",
            "technological dependence"
        ]
    },

    # WEEK 2 – City, Society, Environment
    8: {
        "name": "Environment",
        "category": "City, Society, Environment",
        "week": 2,
        "key_areas": [
            "Environmental problems",
            "Climate change",
            "Conservation",
            "Sustainability"
        ],
        "vocabulary": [
            "environmental degradation",
            "climate change",
            "global warming",
            "carbon footprint",
            "renewable energy",
            "sustainable development",
            "biodiversity",
            "deforestation",
            "pollution control",
            "eco-friendly"
        ]
    },
    9: {
        "name": "Transport",
        "category": "City, Society, Environment",
        "week": 2,
        "key_areas": [
            "Public vs private transport",
            "Traffic problems",
            "Transportation infrastructure",
            "Future of transport"
        ],
        "vocabulary": [
            "public transport",
            "traffic congestion",
            "carbon emissions",
            "transportation infrastructure",
            "commuting",
            "rush hour",
            "mass transit",
            "environmentally friendly",
            "traffic jam",
            "road network"
        ]
    },
    10: {
        "name": "Travel",
        "category": "City, Society, Environment",
        "week": 2,
        "key_areas": [
            "Types of travel",
            "Tourism benefits and drawbacks",
            "Cultural exchange",
            "Travel experiences"
        ],
        "vocabulary": [
            "tourist destination",
            "cultural exchange",
            "travel industry",
            "mass tourism",
            "eco-tourism",
            "travel experience",
            "local customs",
            "tourism revenue",
            "tourist attraction",
            "adventure tourism"
        ]
    },
    11: {
        "name": "Home / Accommodation",
        "category": "City, Society, Environment",
        "week": 2,
        "key_areas": [
            "Types of housing",
            "Living conditions",
            "Urban vs rural living",
            "Housing issues"
        ],
        "vocabulary": [
            "residential area",
            "housing shortage",
            "property market",
            "living conditions",
            "accommodation",
            "rented accommodation",
            "home ownership",
            "urban dwelling",
            "spacious",
            "affordable housing"
        ]
    },
    12: {
        "name": "Shopping / Money",
        "category": "City, Society, Environment",
        "week": 2,
        "key_areas": [
            "Shopping habits",
            "Consumer culture",
            "Financial management",
            "Online vs offline shopping"
        ],
        "vocabulary": [
            "consumer goods",
            "shopping habits",
            "impulse buying",
            "brand loyalty",
            "online shopping",
            "financial management",
            "cost of living",
            "disposable income",
            "purchasing power",
            "consumer society"
        ]
    },
    13: {
        "name": "Society",
        "category": "City, Society, Environment",
        "week": 2,
        "key_areas": [
            "Social issues",
            "Community life",
            "Social changes",
            "Modern society"
        ],
        "vocabulary": [
            "social cohesion",
            "community spirit",
            "social inequality",
            "modern society",
            "social norms",
            "cultural diversity",
            "generation gap",
            "social interaction",
            "social values",
            "community involvement"
        ]
    },
    14: {
        "name": "Crime & Law",
        "category": "City, Society, Environment",
        "week": 2,
        "key_areas": [
            "Types of crime",
            "Law enforcement",
            "Justice system",
            "Crime prevention"
        ],
        "vocabulary": [
            "criminal activity",
            "law enforcement",
            "crime prevention",
            "legal system",
            "juvenile crime",
            "crime rate",
            "punishment",
            "rehabilitation",
            "public safety",
            "law-abiding citizen"
        ]
    },

    # WEEK 3 – Science, Culture, Media
    15: {
        "name": "Media & Advertising",
        "category": "Science, Culture, Media",
        "week": 3,
        "key_areas": [
            "Mass media",
            "Advertising influence",
            "News and information",
            "Media impact on society"
        ],
        "vocabulary": [
            "mass media",
            "advertising campaign",
            "consumer behavior",
            "media coverage",
            "fake news",
            "freedom of press",
            "media influence",
            "target audience",
            "marketing strategy",
            "media literacy"
        ]
    },
    16: {
        "name": "Culture & Traditions",
        "category": "Science, Culture, Media",
        "week": 3,
        "key_areas": [
            "Cultural heritage",
            "Traditions and customs",
            "Cultural preservation",
            "Cultural diversity"
        ],
        "vocabulary": [
            "cultural heritage",
            "traditional customs",
            "cultural identity",
            "cultural diversity",
            "cultural preservation",
            "indigenous culture",
            "cultural exchange",
            "ancestral traditions",
            "cultural values",
            "multicultural society"
        ]
    },
    17: {
        "name": "Science",
        "category": "Science, Culture, Media",
        "week": 3,
        "key_areas": [
            "Scientific research",
            "Scientific discoveries",
            "Science and society",
            "Science education"
        ],
        "vocabulary": [
            "scientific research",
            "breakthrough",
            "innovation",
            "scientific method",
            "research findings",
            "technological advancement",
            "scientific knowledge",
            "empirical evidence",
            "scientific community",
            "research funding"
        ]
    },
    18: {
        "name": "Technology (Advanced)",
        "category": "Science, Culture, Media",
        "week": 3,
        "key_areas": [
            "Artificial Intelligence",
            "Automation",
            "Digital transformation",
            "Future technology"
        ],
        "vocabulary": [
            "artificial intelligence",
            "automation",
            "machine learning",
            "digital transformation",
            "technological disruption",
            "data privacy",
            "cybersecurity",
            "virtual reality",
            "smart devices",
            "technological revolution"
        ]
    },
    19: {
        "name": "Global Issues",
        "category": "Science, Culture, Media",
        "week": 3,
        "key_areas": [
            "International problems",
            "Global challenges",
            "International cooperation",
            "World affairs"
        ],
        "vocabulary": [
            "global warming",
            "poverty alleviation",
            "humanitarian crisis",
            "international cooperation",
            "developing countries",
            "global economy",
            "world peace",
            "natural disasters",
            "refugee crisis",
            "sustainable development"
        ]
    },
    20: {
        "name": "Economy",
        "category": "Science, Culture, Media",
        "week": 3,
        "key_areas": [
            "Economic systems",
            "Economic development",
            "Financial markets",
            "Economic challenges"
        ],
        "vocabulary": [
            "economic growth",
            "economic development",
            "financial stability",
            "market economy",
            "economic recession",
            "inflation rate",
            "unemployment",
            "economic inequality",
            "GDP",
            "economic prosperity"
        ]
    },
    21: {
        "name": "Education (Advanced)",
        "category": "Science, Culture, Media",
        "week": 3,
        "key_areas": [
            "Higher education",
            "Education reform",
            "Online learning",
            "Educational challenges"
        ],
        "vocabulary": [
            "tertiary education",
            "academic excellence",
            "education reform",
            "online learning",
            "vocational training",
            "educational resources",
            "student debt",
            "academic pressure",
            "quality education",
            "educational inequality"
        ]
    },

    # WEEK 4 – Advanced Writing Topics
    22: {
        "name": "Government & Politics",
        "category": "Advanced Writing Topics",
        "week": 4,
        "key_areas": [
            "Political systems",
            "Government policies",
            "Democratic processes",
            "Public administration"
        ],
        "vocabulary": [
            "government policy",
            "political system",
            "democratic process",
            "public administration",
            "legislation",
            "policy implementation",
            "government spending",
            "political stability",
            "public sector",
            "governance"
        ]
    },
    23: {
        "name": "Environment (Advanced)",
        "category": "Advanced Writing Topics",
        "week": 4,
        "key_areas": [
            "Environmental policies",
            "Climate action",
            "Green technology",
            "Environmental activism"
        ],
        "vocabulary": [
            "environmental policy",
            "climate action",
            "carbon neutrality",
            "green technology",
            "environmental protection",
            "ecological balance",
            "waste management",
            "environmental awareness",
            "sustainable practices",
            "ecosystem"
        ]
    },
    24: {
        "name": "Health (Advanced)",
        "category": "Advanced Writing Topics",
        "week": 4,
        "key_areas": [
            "Public health",
            "Healthcare policies",
            "Medical research",
            "Health challenges"
        ],
        "vocabulary": [
            "public health",
            "healthcare provision",
            "medical breakthrough",
            "preventive medicine",
            "health epidemic",
            "medical research",
            "healthcare funding",
            "health awareness",
            "mental health issues",
            "healthcare accessibility"
        ]
    },
    25: {
        "name": "Employment",
        "category": "Advanced Writing Topics",
        "week": 4,
        "key_areas": [
            "Job market trends",
            "Employment policies",
            "Future of work",
            "Workplace issues"
        ],
        "vocabulary": [
            "labor market",
            "employment opportunities",
            "job creation",
            "workforce",
            "remote working",
            "gig economy",
            "employment rights",
            "workplace diversity",
            "career development",
            "job displacement"
        ]
    },
    26: {
        "name": "Art & Entertainment",
        "category": "Advanced Writing Topics",
        "week": 4,
        "key_areas": [
            "Art and culture",
            "Entertainment industry",
            "Cultural activities",
            "Arts funding"
        ],
        "vocabulary": [
            "artistic expression",
            "cultural significance",
            "entertainment industry",
            "performing arts",
            "visual arts",
            "cultural venue",
            "artistic talent",
            "creative industry",
            "arts funding",
            "cultural event"
        ]
    },
    27: {
        "name": "Technology & Future",
        "category": "Advanced Writing Topics",
        "week": 4,
        "key_areas": [
            "Future predictions",
            "Technological impact",
            "Digital future",
            "Innovation"
        ],
        "vocabulary": [
            "future prospects",
            "technological innovation",
            "digital age",
            "emerging technology",
            "technological progress",
            "future generations",
            "scientific advancement",
            "tech industry",
            "digital economy",
            "innovation hub"
        ]
    },
    28: {
        "name": "Social Media",
        "category": "Advanced Writing Topics",
        "week": 4,
        "key_areas": [
            "Social media influence",
            "Online communication",
            "Digital society",
            "Social media challenges"
        ],
        "vocabulary": [
            "social networking",
            "online presence",
            "digital communication",
            "viral content",
            "online community",
            "social media platform",
            "digital footprint",
            "online harassment",
            "information sharing",
            "social media influencer"
        ]
    },
    29: {
        "name": "Education vs Work",
        "category": "Advanced Writing Topics",
        "week": 4,
        "key_areas": [
            "Academic vs practical skills",
            "Work experience",
            "Career preparation",
            "Education value"
        ],
        "vocabulary": [
            "academic qualifications",
            "work experience",
            "practical skills",
            "career preparation",
            "job-specific training",
            "theoretical knowledge",
            "professional skills",
            "employability",
            "skill development",
            "workplace readiness"
        ]
    },
    30: {
        "name": "Review & Consolidation",
        "category": "Final Review",
        "week": 4,
        "key_areas": [
            "Review all topics",
            "Practice using vocabulary",
            "Consolidate learning",
            "Prepare for exam"
        ],
        "vocabulary": [
            "comprehensive review",
            "vocabulary retention",
            "topic mastery",
            "exam preparation",
            "practice exercises",
            "skill consolidation",
            "language proficiency",
            "test strategies",
            "performance improvement",
            "confidence building"
        ]
    }
}


def get_current_day_number(start_date: date = None) -> int:
    """
    Get current day number in the 30-day plan
    If start_date is None, use a default start date or cycle through days
    """
    if start_date is None:
        # Use day of year modulo 30 to cycle through topics
        today = date.today()
        day_of_year = today.timetuple().tm_yday
        return (day_of_year % 30) + 1
    else:
        today = date.today()
        days_passed = (today - start_date).days
        current_day = (days_passed % 30) + 1
        return current_day


def get_topic_for_day(day_number: int) -> Dict:
    """Get topic information for a specific day"""
    return TOPICS_PLAN.get(day_number, TOPICS_PLAN[1])


def get_current_topic(start_date: date = None) -> Dict:
    """Get today's topic based on the 30-day plan"""
    day_number = get_current_day_number(start_date)
    return get_topic_for_day(day_number)


def format_topic_message(topic: Dict, day_number: int) -> str:
    """Format topic information as a message"""
    message = f"""
📚 **IELTS Vocabulary - Day {day_number}/30**

🎯 **Topic: {topic['name']}**
📂 Category: {topic['category']}
📅 Week {topic['week']}

**Key Areas to Study:**
"""

    for i, area in enumerate(topic['key_areas'], 1):
        message += f"{i}. {area}\n"

    message += "\n**Essential Vocabulary:**\n"

    # Split vocabulary into two columns for better readability
    vocab = topic['vocabulary']
    mid = len(vocab) // 2

    for i in range(mid):
        left = f"• {vocab[i]}"
        right = f"• {vocab[i + mid]}" if i + mid < len(vocab) else ""
        message += f"{left:<30} {right}\n"

    message += """
💡 **Study Tips:**
1. Learn the meaning and usage of each word
2. Practice using words in sentences
3. Review yesterday's vocabulary
4. Use words in speaking/writing practice

Good luck with today's vocabulary! 🎯
"""

    return message
