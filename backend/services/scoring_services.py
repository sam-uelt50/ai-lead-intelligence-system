# backend/services/scoring_service.py
from datetime import datetime
from typing import Dict, Any, List
import math

from config import config
from database.models.signal import SignalType

class ScoringService:
    """Score companies based on growth signals"""
    
    def __init__(self):
        self.weights = config.SCORING_WEIGHTS
        
    def calculate_company_score(self, company: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate all scores for a company"""
        signals = company.get("growth_signals", [])
        
        # Base score starts at 30
        base_score = 30.0
        
        # Calculate signal-based scores
        signal_scores = self._calculate_signal_scores(signals)
        
        # Calculate timing score
        timing_score = self._calculate_timing_score(signals, company)
        
        # Calculate fit score (ICP match)
        fit_score = self._calculate_fit_score(company)
        
        # Weighted total score
        weighted_score = (
            signal_scores["total"] * 0.6 +
            timing_score * 0.25 +
            fit_score * 0.15
        )
        
        # Cap at 100
        final_score = min(100, base_score + weighted_score)
        
        # Determine priority
        priority = self._determine_priority(final_score, len(signals))
        
        return {
            "score": round(final_score),
            "priority": priority,
            "breakdown": {
                "signal_score": round(signal_scores["total"]),
                "timing_score": round(timing_score),
                "fit_score": round(fit_score),
                "signal_details": signal_scores["by_type"]
            },
            "recommended_actions": self._get_recommended_actions(final_score, signals)
        }
    
    def _calculate_signal_scores(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate scores based on detected signals"""
        scores_by_type = {}
        total_score = 0.0
        
        for signal in signals:
            signal_type = signal.get("type")
            confidence = signal.get("confidence", 50) / 100.0
            
            # Base score for each signal type
            type_weights = {
                SignalType.HIRING.value: 25,
                SignalType.FUNDING.value: 30,
                SignalType.TECH_REFRESH.value: 20,
                SignalType.EXPANSION.value: 15,
                SignalType.LEADERSHIP_CHANGE.value: 10
            }
            
            base_score = type_weights.get(signal_type, 10)
            
            # Apply confidence
            signal_score = base_score * confidence
            
            # Recency bonus (signals detected in last 30 days)
            detected_at = signal.get("detected_at")
            if isinstance(detected_at, str):
                detected_at = datetime.fromisoformat(detected_at.replace("Z", "+00:00"))
            
            if isinstance(detected_at, datetime):
                days_ago = (datetime.now() - detected_at).days
                if days_ago <= 30:
                    recency_bonus = (30 - days_ago) * 0.5  # Up to 15 points
                    signal_score += recency_bonus
            
            # Cap individual signal score
            signal_score = min(50, signal_score)
            
            # Add to totals
            scores_by_type[signal_type] = scores_by_type.get(signal_type, 0) + signal_score
            total_score += signal_score
        
        # Cap total signal score
        total_score = min(70, total_score)
        
        return {
            "total": total_score,
            "by_type": scores_by_type
        }
    
    def _calculate_timing_score(self, signals: List[Dict[str, Any]], company: Dict[str, Any]) -> float:
        """Calculate timing score (is now a good time?)"""
        if not signals:
            return 30.0
        
        score = 40.0
        now = datetime.now()
        
        # Recent signal bonus
        recent_signals = 0
        for signal in signals:
            detected_at = signal.get("detected_at")
            if isinstance(detected_at, str):
                detected_at = datetime.fromisoformat(detected_at.replace("Z", "+00:00"))
            
            if isinstance(detected_at, datetime):
                days_ago = (now - detected_at).days
                if days_ago <= 14:  # Signals in last 2 weeks
                    recent_signals += 1
        
        # Bonus for multiple recent signals
        score += min(recent_signals * 10, 30)
        
        # Seasonal adjustment (Q1/Q2 are generally better)
        quarter = (now.month - 1) // 3 + 1
        if quarter in [1, 2]:  # Q1, Q2
            score += 15
        elif quarter == 4:  # Q4
            score -= 10
        
        return min(100, score)
    
    def _calculate_fit_score(self, company: Dict[str, Any]) -> float:
        """Calculate fit with agency's ICP"""
        score = 50.0  # Neutral
        
        # Size fit
        size = company.get("size", "")
        if size:
            # Parse employee range (e.g., "51-200 employees")
            import re
            match = re.search(r"(\d+)-(\d+)", size)
            if match:
                min_emp, max_emp = int(match.group(1)), int(match.group(2))
                
                # Ideal: 10-500 employees
                if min_emp >= 10 and max_emp <= 500:
                    score += 25
                elif min_emp >= 5 and max_emp <= 1000:
                    score += 10
        
        # Industry fit
        industry = company.get("industry", "").lower()
        target_industries = [i.lower() for i in config.DEFAULT_ICP["target_industries"]]
        excluded_industries = [i.lower() for i in config.DEFAULT_ICP["excluded_industries"]]
        
        if industry in excluded_industries:
            score -= 20
        elif any(target in industry for target in target_industries):
            score += 15
        
        # Website quality check
        website = company.get("website", "")
        if website and website.startswith("https://"):
            score += 5
        
        return min(100, max(0, score))
    
    def _determine_priority(self, score: float, signal_count: int) -> str:
        """Determine priority level based on score and signals"""
        if score >= config.PRIORITY_THRESHOLDS["hot"] and signal_count >= 2:
            return "hot"
        elif score >= config.PRIORITY_THRESHOLDS["warm"]:
            return "warm"
        elif score >= config.PRIORITY_THRESHOLDS["cold"]:
            return "cold"
        else:
            return "excluded"
    
    def _get_recommended_actions(self, score: float, signals: List[Dict[str, Any]]) -> List[str]:
        """Get recommended actions based on score"""
        actions = []
        
        if score >= 80:
            actions.extend([
                "Immediate outreach recommended",
                "Schedule intro call this week",
                "Prepare personalized research brief"
            ])
        elif score >= 60:
            actions.extend([
                "Add to outreach queue for next 2 weeks",
                "Research decision makers",
                "Prepare value proposition"
            ])
        else:
            actions.extend([
                "Monitor for additional signals",
                "Consider re-evaluating in 30 days"
            ])
        
        # Signal-specific actions
        signal_types = {s.get("type") for s in signals}
        
        if SignalType.HIRING.value in signal_types:
            actions.append("Reference new hiring in outreach")
        
        if SignalType.FUNDING.value in signal_types:
            actions.append("Congratulate on recent funding")
        
        if SignalType.TECH_REFRESH.value in signal_types:
            actions.append("Offer help with new tech stack")
        
        return actions
