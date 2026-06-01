def classify_technical_strength(technical_result):
    score = technical_result["score"]
    max_score = technical_result["max_score"]
    strength = (score / max_score) * 100

    if strength >= 70:
        return "Strong Technicals", strength

    if strength >= 50:
        return "Mixed Technicals", strength

    return "Weak Technicals", strength


def classify_fundamental_strength(fundamental_score):
    score = fundamental_score["score"]
    max_score = fundamental_score["max_score"]
    strength = (score / max_score) * 100

    if strength >= 70:
        return "Strong Fundamentals", strength

    if strength >= 50:
        return "Mixed Fundamentals", strength

    return "Weak Fundamentals", strength


def get_conflict_view(technical_result, fundamental_score):
    technical_label, technical_strength = classify_technical_strength(technical_result)
    fundamental_label, fundamental_strength = classify_fundamental_strength(fundamental_score)

    technical_is_strong = technical_strength >= 70
    technical_is_weak = technical_strength < 50

    fundamental_is_strong = fundamental_strength >= 70
    fundamental_is_weak = fundamental_strength < 50

    if fundamental_is_strong and technical_is_strong:
        verdict = "Strong Business + Strong Chart"
        action_view = "Best Setup"
        explanation = (
            "The company shows strong fundamentals and the chart also confirms strength. "
            "This is usually the highest-quality setup, but entry price and risk should still be checked."
        )
    elif fundamental_is_strong and technical_is_weak:
        verdict = "Strong Business + Weak Chart"
        action_view = "Good Company, Wait for Entry"
        explanation = (
            "The business looks fundamentally strong, but the chart is not supporting an entry yet. "
            "This may be a good watchlist candidate until price action improves."
        )
    elif fundamental_is_weak and technical_is_strong:
        verdict = "Weak Business + Strong Chart"
        action_view = "Momentum Trade Only"
        explanation = (
            "The chart is strong, but fundamentals are weak. This may work as a short-term momentum trade, "
            "but it is not ideal for long-term investing without deeper research."
        )
    elif fundamental_is_weak and technical_is_weak:
        verdict = "Weak Business + Weak Chart"
        action_view = "Avoid / Low Priority"
        explanation = (
            "Both fundamentals and technicals are weak. This stock is low priority unless something changes."
        )
    else:
        verdict = f"{fundamental_label} + {technical_label}"
        action_view = "Watchlist / Needs Confirmation"
        explanation = (
            "The stock has a mixed setup. It needs either stronger fundamentals, stronger price action, "
            "or a better entry zone before becoming attractive."
        )

    return {
        "verdict": verdict,
        "action_view": action_view,
        "technical_label": technical_label,
        "technical_strength": technical_strength,
        "fundamental_label": fundamental_label,
        "fundamental_strength": fundamental_strength,
        "explanation": explanation,
    }
    
def get_entry_quality(technical_result):
    current_price = technical_result["current_price"]
    dma_50 = technical_result["dma_50"]
    dma_200 = technical_result["dma_200"]
    support = technical_result["support"]
    resistance = technical_result["resistance"]
    rsi = technical_result["rsi"]
    volume_ratio = technical_result["volume_ratio"]

    distance_from_support = ((current_price - support) / support) * 100
    distance_from_resistance = ((resistance - current_price) / current_price) * 100

    score = 0
    max_score = 5
    reasons = []

    if current_price > dma_200:
        score += 1
        reasons.append("Price is above the 200 DMA, so the long-term trend supports entry.")
    else:
        reasons.append("Price is below the 200 DMA, so entry is risky until the long-term trend improves.")

    if current_price > dma_50:
        score += 1
        reasons.append("Price is above the 50 DMA, showing short-to-medium term strength.")
    else:
        reasons.append("Price is below the 50 DMA, so short-term momentum is weak.")

    if distance_from_support <= 8:
        score += 1
        reasons.append("Price is reasonably close to support, so risk can be managed better.")
    elif distance_from_resistance <= 5:
        reasons.append("Price is close to resistance, so this may be a chase entry.")
    else:
        reasons.append("Price is between support and resistance, so entry is neutral.")

    if 45 <= rsi <= 65:
        score += 1
        reasons.append("RSI is in a healthy range, not too weak and not too overextended.")
    elif rsi > 70:
        reasons.append("RSI is above 70, so the stock may be overextended in the short term.")
    else:
        reasons.append("RSI is weak, so momentum confirmation is missing.")

    if volume_ratio >= 1.2:
        score += 1
        reasons.append("Volume is above average, supporting the price move.")
    else:
        reasons.append("Volume is below confirmation level, so entry lacks strong participation.")

    strength = (score / max_score) * 100

    if strength >= 80:
        entry_label = "Good Entry Zone"
    elif strength >= 60:
        entry_label = "Acceptable Entry"
    elif distance_from_resistance <= 5 or rsi > 70:
        entry_label = "Chase Entry Risk"
    elif strength >= 40:
        entry_label = "Wait for Confirmation"
    else:
        entry_label = "Poor Entry Setup"

    return {
        "score": score,
        "max_score": max_score,
        "strength": strength,
        "entry_label": entry_label,
        "reasons": reasons,
        "distance_from_support": distance_from_support,
        "distance_from_resistance": distance_from_resistance,
    }
def get_watchlist_triggers(technical_result):
    current_price = technical_result["current_price"]
    dma_50 = technical_result["dma_50"]
    dma_200 = technical_result["dma_200"]
    support = technical_result["support"]
    resistance = technical_result["resistance"]
    rsi = technical_result["rsi"]
    volume_ratio = technical_result["volume_ratio"]

    triggers = []

    if current_price < dma_200:
        triggers.append({
            "Trigger": "Reclaim 200 DMA",
            "Type": "Bullish Confirmation",
            "Level / Condition": f"Close above {dma_200:.2f}",
            "Why it matters": "A close above the 200 DMA would indicate improving long-term trend.",
        })
    else:
        triggers.append({
            "Trigger": "Hold Above 200 DMA",
            "Type": "Trend Protection",
            "Level / Condition": f"Stay above {dma_200:.2f}",
            "Why it matters": "Holding above the 200 DMA keeps the long-term uptrend intact.",
        })

    if current_price < dma_50:
        triggers.append({
            "Trigger": "Reclaim 50 DMA",
            "Type": "Short-Term Strength",
            "Level / Condition": f"Close above {dma_50:.2f}",
            "Why it matters": "A close above the 50 DMA would show improving short-term momentum.",
        })
    else:
        triggers.append({
            "Trigger": "Hold Above 50 DMA",
            "Type": "Momentum Protection",
            "Level / Condition": f"Stay above {dma_50:.2f}",
            "Why it matters": "Holding above the 50 DMA keeps short-term strength intact.",
        })

    triggers.append({
        "Trigger": "Support Breakdown",
        "Type": "Risk Alert",
        "Level / Condition": f"Close below {support:.2f}",
        "Why it matters": "A close below support would show sellers gaining control.",
    })

    triggers.append({
        "Trigger": "Resistance Breakout",
        "Type": "Bullish Breakout",
        "Level / Condition": f"Close above {resistance:.2f}",
        "Why it matters": "A resistance breakout can signal a new upward move.",
    })

    if volume_ratio < 1.2:
        triggers.append({
            "Trigger": "Volume Confirmation",
            "Type": "Participation Check",
            "Level / Condition": "Volume above 1.5x 20-day average",
            "Why it matters": "Higher volume confirms that institutions or larger buyers may be participating.",
        })
    else:
        triggers.append({
            "Trigger": "Sustain Volume Strength",
            "Type": "Participation Check",
            "Level / Condition": "Keep volume above average",
            "Why it matters": "Sustained higher volume supports stronger price movement.",
        })

    if rsi < 45:
        triggers.append({
            "Trigger": "RSI Recovery",
            "Type": "Momentum Check",
            "Level / Condition": "RSI above 50",
            "Why it matters": "RSI moving above 50 would show improving momentum.",
        })
    elif rsi > 70:
        triggers.append({
            "Trigger": "RSI Cool-Off",
            "Type": "Overextension Check",
            "Level / Condition": "RSI cools below 65 without price breakdown",
            "Why it matters": "A cool-off without price damage can create a healthier entry.",
        })
    else:
        triggers.append({
            "Trigger": "RSI Strength",
            "Type": "Momentum Check",
            "Level / Condition": "RSI stays above 50",
            "Why it matters": "RSI above 50 supports positive momentum.",
        })

    return triggers

def generate_investment_memo(technical_result, fundamental_score, conflict_view, entry_quality):
    technical_strength = (technical_result["score"] / technical_result["max_score"]) * 100
    fundamental_strength = (fundamental_score["score"] / fundamental_score["max_score"]) * 100

    if technical_strength >= 70:
        technical_summary = "The technical setup is strong. Price action supports the stock."
    elif technical_strength >= 50:
        technical_summary = "The technical setup is mixed. Some signals are positive, but confirmation is still needed."
    else:
        technical_summary = "The technical setup is weak. Price action does not strongly support entry yet."

    if fundamental_strength >= 70:
        fundamental_summary = "The business quality looks strong based on available fundamental data."
    elif fundamental_strength >= 50:
        fundamental_summary = "The business quality looks average or mixed based on available fundamental data."
    else:
        fundamental_summary = "The business quality looks weak or data is insufficient based on available fundamental data."

    entry_label = entry_quality["entry_label"]

    if entry_label in ["Good Entry Zone", "Acceptable Entry"]:
        entry_summary = "The current price appears reasonably suitable for entry based on trend, support, RSI, and volume."
    elif entry_label == "Chase Entry Risk":
        entry_summary = "The stock may be extended near resistance or high RSI, so entry risk is elevated."
    else:
        entry_summary = "The current price does not offer a strong entry setup yet."

    if technical_strength >= 70 and fundamental_strength >= 70 and entry_quality["strength"] >= 60:
        final_note = "This is a high-priority research candidate. It has a strong chart, strong fundamentals, and acceptable entry quality."
    elif fundamental_strength >= 70 and technical_strength < 50:
        final_note = "This may be a good business but not a good technical entry yet. Add it to watchlist and wait for trend confirmation."
    elif technical_strength >= 70 and fundamental_strength < 50:
        final_note = "This looks more suitable as a momentum trade than a long-term investment candidate."
    elif entry_quality["strength"] < 40:
        final_note = "Entry quality is weak, so waiting for a better setup may be safer."
    else:
        final_note = "This is a watchlist candidate. More confirmation is needed before treating it as a strong setup."

    return {
        "Overall View": conflict_view["action_view"],
        "Technical View": technical_summary,
        "Fundamental View": fundamental_summary,
        "Entry View": entry_summary,
        "Main Risk": "The signal can fail if price breaks key support, volume remains weak, or fundamentals deteriorate.",
        "What To Watch": "Watch 50 DMA, 200 DMA, support, resistance, volume confirmation, and RSI strength.",
        "Final Research Note": final_note,
    }