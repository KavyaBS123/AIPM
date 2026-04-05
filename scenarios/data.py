"""Scenario data for AI Product Manager Environment."""

import json
from typing import List, Dict, Any
from pathlib import Path


SCENARIOS = {
    "scenario_1_ecommerce": {
        "name": "E-Commerce Platform Growth",
        "description": "Growing e-commerce platform with declining order completion rates",
        "user_feedback": [
            {
                "complaint": "Checkout process is too slow and convoluted",
                "severity": 0.9,
                "frequency": 238,
                "sentiment": "negative"
            },
            {
                "complaint": "Missing recommended products based on browsing history",
                "severity": 0.7,
                "frequency": 156,
                "sentiment": "negative"
            },
            {
                "complaint": "Wish list feature is buggy and doesn't save items",
                "severity": 0.8,
                "frequency": 89,
                "sentiment": "negative"
            },
            {
                "complaint": "Mobile app is much slower than web version",
                "severity": 0.75,
                "frequency": 204,
                "sentiment": "negative"
            },
            {
                "complaint": "Love the new dark mode!",
                "severity": 0.3,
                "frequency": 45,
                "sentiment": "positive"
            }
        ],
        "metrics": {
            "churn_rate": 0.25,
            "retention_rate": 0.75,
            "revenue": 450000,
            "user_satisfaction": 0.62,
            "engagement_score": 0.58,
            "active_users": 12500
        },
        "features": [
            {
                "feature_id": "F001",
                "name": "One-Click Checkout",
                "description": "Implement one-click checkout with saved payment methods",
                "impact_on_satisfaction": 0.35,
                "impact_on_revenue": 0.25,
                "impact_on_churn": -0.30,
                "effort": 45,
                "risk": 0.2,
                "user_requests": 350,
                "priority_score": None
            },
            {
                "feature_id": "F002",
                "name": "AI-Powered Recommendations",
                "description": "ML-based product recommendations using browsing and purchase history",
                "impact_on_satisfaction": 0.28,
                "impact_on_revenue": 0.40,
                "impact_on_churn": -0.15,
                "effort": 60,
                "risk": 0.35,
                "user_requests": 210,
                "priority_score": None
            },
            {
                "feature_id": "F003",
                "name": "Wishlist Enhancement",
                "description": "Fix and enhance wish list functionality with sharing capabilities",
                "impact_on_satisfaction": 0.15,
                "impact_on_revenue": 0.05,
                "impact_on_churn": -0.08,
                "effort": 20,
                "risk": 0.1,
                "user_requests": 125,
                "priority_score": None
            },
            {
                "feature_id": "F004",
                "name": "Mobile App Optimization",
                "description": "Performance optimization for mobile app (database indexing, caching)",
                "impact_on_satisfaction": 0.25,
                "impact_on_revenue": 0.15,
                "impact_on_churn": -0.20,
                "effort": 55,
                "risk": 0.15,
                "user_requests": 300,
                "priority_score": None
            },
            {
                "feature_id": "F005",
                "name": "Subscription Plans",
                "description": "Add subscription models for recurring purchases",
                "impact_on_satisfaction": 0.10,
                "impact_on_revenue": 0.50,
                "impact_on_churn": -0.05,
                "effort": 75,
                "risk": 0.4,
                "user_requests": 50,
                "priority_score": None
            }
        ],
        "constraints": {
            "sprint_duration": 2,
            "team_capacity": 200,
            "budget_available": 80000,
            "deadline": None,
            "max_parallel_features": 2
        }
    },
    "scenario_2_saas": {
        "name": "SaaS Analytics Platform",
        "description": "Data analytics SaaS experiencing plateau in growth",
        "user_feedback": [
            {
                "complaint": "Dashboard customization is confusing and limited",
                "severity": 0.7,
                "frequency": 78,
                "sentiment": "negative"
            },
            {
                "complaint": "Export to PDF/Excel is broken and slow",
                "severity": 0.85,
                "frequency": 142,
                "sentiment": "negative"
            },
            {
                "complaint": "API rate limits are too restrictive",
                "severity": 0.75,
                "frequency": 34,
                "sentiment": "negative"
            },
            {
                "complaint": "Excellent data visualization improvements",
                "severity": 0.2,
                "frequency": 95,
                "sentiment": "positive"
            },
            {
                "complaint": "Need multi-workspace support for teams",
                "severity": 0.8,
                "frequency": 56,
                "sentiment": "negative"
            }
        ],
        "metrics": {
            "churn_rate": 0.18,
            "retention_rate": 0.82,
            "revenue": 280000,
            "user_satisfaction": 0.71,
            "engagement_score": 0.68,
            "active_users": 8300
        },
        "features": [
            {
                "feature_id": "F101",
                "name": "Custom Dashboard Builder",
                "description": "Drag-and-drop dashboard customization with preset templates",
                "impact_on_satisfaction": 0.32,
                "impact_on_revenue": 0.20,
                "impact_on_churn": -0.22,
                "effort": 50,
                "risk": 0.2,
                "user_requests": 120,
                "priority_score": None
            },
            {
                "feature_id": "F102",
                "name": "Advanced Export Formats",
                "description": "Fix and optimize PDF/Excel/PowerPoint export with scheduling",
                "impact_on_satisfaction": 0.38,
                "impact_on_revenue": 0.10,
                "impact_on_churn": -0.18,
                "effort": 35,
                "risk": 0.12,
                "user_requests": 180,
                "priority_score": None
            },
            {
                "feature_id": "F103",
                "name": "API v2 Release",
                "description": "New API version with higher rate limits and better documentation",
                "impact_on_satisfaction": 0.25,
                "impact_on_revenue": 0.35,
                "impact_on_churn": -0.10,
                "effort": 70,
                "risk": 0.3,
                "user_requests": 60,
                "priority_score": None
            },
            {
                "feature_id": "F104",
                "name": "Multi-Workspace Collaboration",
                "description": "Enable team collaboration with role-based access control",
                "impact_on_satisfaction": 0.40,
                "impact_on_revenue": 0.45,
                "impact_on_churn": -0.25,
                "effort": 80,
                "risk": 0.35,
                "user_requests": 85,
                "priority_score": None
            },
            {
                "feature_id": "F105",
                "name": "Real-time Alerts",
                "description": "Real-time anomaly detection and alerts for key metrics",
                "impact_on_satisfaction": 0.22,
                "impact_on_revenue": 0.25,
                "impact_on_churn": -0.15,
                "effort": 55,
                "risk": 0.4,
                "user_requests": 95,
                "priority_score": None
            }
        ],
        "constraints": {
            "sprint_duration": 2,
            "team_capacity": 160,
            "budget_available": 60000,
            "deadline": None,
            "max_parallel_features": 2
        }
    },
    "scenario_3_social": {
        "name": "Social Network Platform",
        "description": "Mature social platform facing engagement decline",
        "user_feedback": [
            {
                "complaint": "Too many ads in feed",
                "severity": 0.9,
                "frequency": 523,
                "sentiment": "negative"
            },
            {
                "complaint": "Content discovery is poor, same content repeatedly",
                "severity": 0.8,
                "frequency": 412,
                "sentiment": "negative"
            },
            {
                "complaint": "Privacy controls are confusing",
                "severity": 0.75,
                "frequency": 198,
                "sentiment": "negative"
            },
            {
                "complaint": "Love the new story features!",
                "severity": 0.2,
                "frequency": 289,
                "sentiment": "positive"
            },
            {
                "complaint": "Need better moderation against hate speech",
                "severity": 0.85,
                "frequency": 256,
                "sentiment": "negative"
            }
        ],
        "metrics": {
            "churn_rate": 0.35,
            "retention_rate": 0.65,
            "revenue": 2100000,
            "user_satisfaction": 0.55,
            "engagement_score": 0.52,
            "active_users": 89000
        },
        "features": [
            {
                "feature_id": "F201",
                "name": "Smart Feed Algorithm",
                "description": "ML-based feed ranking to avoid repeated content",
                "impact_on_satisfaction": 0.35,
                "impact_on_revenue": 0.05,
                "impact_on_churn": -0.28,
                "effort": 65,
                "risk": 0.4,
                "user_requests": 520,
                "priority_score": None
            },
            {
                "feature_id": "F202",
                "name": "Ad Frequency Control",
                "description": "Allow users to control frequency of ads in their feed",
                "impact_on_satisfaction": 0.45,
                "impact_on_revenue": -0.20,
                "impact_on_churn": -0.35,
                "effort": 30,
                "risk": 0.1,
                "user_requests": 685,
                "priority_score": None
            },
            {
                "feature_id": "F203",
                "name": "Privacy Dashboard",
                "description": "Simplified privacy controls and transparency center",
                "impact_on_satisfaction": 0.30,
                "impact_on_revenue": -0.05,
                "impact_on_churn": -0.15,
                "effort": 40,
                "risk": 0.15,
                "user_requests": 245,
                "priority_score": None
            },
            {
                "feature_id": "F204",
                "name": "AI Content Moderation",
                "description": "Automated detection and suppression of hate speech",
                "impact_on_satisfaction": 0.28,
                "impact_on_revenue": -0.10,
                "impact_on_churn": -0.18,
                "effort": 75,
                "risk": 0.45,
                "user_requests": 340,
                "priority_score": None
            },
            {
                "feature_id": "F205",
                "name": "Premium Subscription",
                "description": "Ad-free experience with additional features",
                "impact_on_satisfaction": 0.25,
                "impact_on_revenue": 0.60,
                "impact_on_churn": -0.10,
                "effort": 45,
                "risk": 0.25,
                "user_requests": 150,
                "priority_score": None
            }
        ],
        "constraints": {
            "sprint_duration": 2,
            "team_capacity": 300,
            "budget_available": 150000,
            "deadline": None,
            "max_parallel_features": 3
        }
    }
}


def get_scenario(scenario_key: str) -> Dict[str, Any]:
    """Get a scenario by key."""
    if scenario_key not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario_key}. Available: {list(SCENARIOS.keys())}")
    return SCENARIOS[scenario_key]


def list_scenarios() -> List[str]:
    """List all available scenarios."""
    return list(SCENARIOS.keys())


def get_all_scenarios() -> Dict[str, Dict[str, Any]]:
    """Get all scenarios."""
    return SCENARIOS
