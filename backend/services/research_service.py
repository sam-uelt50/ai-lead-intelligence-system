# backend/services/research_service.py
from typing import Dict, Any

class ResearchService:
    """Generate research briefs for companies"""
    
    def generate_brief(self, company: Dict[str, Any]) -> str:
        """Generate a research brief for a company"""
        name = company.get("name", "Company")
        industry = company.get("industry", "Unknown")
        size = company.get("size", "Unknown")
        signals = company.get("growth_signals", [])
        score = company.get("score", 0)
        priority = company.get("priority", "cold")
        
        # Count signals by type
        signal_counts = {}
        for signal in signals:
            sig_type = signal.get("type")
            signal_counts[sig_type] = signal_counts.get(sig_type, 0) + 1
        
        # Generate brief
        brief = f"""# Research Brief: {name}

## Overview
- **Industry:** {industry}
- **Size:** {size}
- **Lead Score:** {score}/100
- **Priority:** {priority.upper()}

## Growth Signals Detected
"""
        
        if signals:
            for sig_type, count in signal_counts.items():
                brief += f"- {count} {sig_type} signal(s)\n"
        else:
            brief += "- No growth signals detected\n"
        
        brief += f"""
## Why Now?
Based on the detected signals, this appears to be a good time for outreach because:
"""
        
        if "hiring" in signal_counts:
            brief += "- They are actively hiring marketing roles, indicating growth and potential budget\n"
        
        if "funding" in signal_counts:
            brief += "- Recent funding suggests available budget and growth ambitions\n"
        
        if "tech_refresh" in signal_counts:
            brief += "- Technology modernization suggests they're investing in growth\n"
        
        if not any(key in signal_counts for key in ["hiring", "funding", "tech_refresh"]):
            brief += "- Company fits target profile based on size and industry\n"
        
        brief += """
## Recommended Approach
1. Reference specific signals in outreach (e.g., "saw you're hiring for marketing roles")
2. Focus on how your services can support their growth phase
3. Suggest a brief introductory call to discuss their current priorities

## Conversation Starters
- "Noticed your recent growth activity, curious about your marketing priorities"
- "We've helped similar companies in your industry with [specific service]"
- "Based on your current phase, we have some ideas that might be relevant"

## Considerations
- Timing might be sensitive depending on their internal priorities
- Ensure outreach is value-focused, not salesy
- Reference verifiable signals rather than generic statements
"""
        
        return brief
