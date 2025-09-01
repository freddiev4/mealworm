from typing import Optional
from .models import WeeklyMealPlan, DayPlan, Meal


class MealPlanFormatter:
    """Formats meal plans into various output formats"""
    
    @staticmethod
    def to_text(plan: WeeklyMealPlan) -> str:
        """Format meal plan as plain text following the Sunday-Saturday-Sunday template"""
        if not plan or not plan.days:
            return "No meal plan available"
        
        output_lines = []
        output_lines.append("🍽️ WEEKLY MEAL PLAN")
        output_lines.append("=" * 30)
        output_lines.append(f"Week starting: {plan.week_starting.strftime('%B %d, %Y')}")
        output_lines.append("")
        
        # Format each day
        for day_plan in plan.days:
            day_line = f"📅 {day_plan.day.upper()}"
            output_lines.append(day_line)
            output_lines.append("-" * len(day_line))
            
            if day_plan.breakfast:
                output_lines.append(f"🌅 Breakfast: {day_plan.breakfast.title}")
            
            if day_plan.lunch:
                output_lines.append(f"☀️ Lunch: {day_plan.lunch.title}")
            
            if day_plan.dinner:
                output_lines.append(f"🌙 Dinner: {day_plan.dinner.title}")
                if day_plan.dinner.cuisine_type:
                    output_lines.append(f"   Cuisine: {day_plan.dinner.cuisine_type}")
                if day_plan.dinner.prep_time:
                    output_lines.append(f"   Prep time: {day_plan.dinner.prep_time} minutes")
            
            if day_plan.snacks:
                snack_names = [snack.title for snack in day_plan.snacks]
                output_lines.append(f"🍿 Snacks: {', '.join(snack_names)}")
            
            if not any([day_plan.breakfast, day_plan.lunch, day_plan.dinner, day_plan.snacks]):
                output_lines.append("   No meals planned")
            
            output_lines.append("")
        
        # Add notes and grocery list if available
        if plan.notes:
            output_lines.append("📝 NOTES")
            output_lines.append("=" * 15)
            output_lines.append(plan.notes)
            output_lines.append("")
        
        if plan.grocery_list:
            output_lines.append("🛒 GROCERY LIST")
            output_lines.append("=" * 20)
            for item in plan.grocery_list:
                output_lines.append(f"• {item}")
        
        return "\n".join(output_lines)
    
    @staticmethod
    def to_simple_template(plan: WeeklyMealPlan) -> str:
        """Format meal plan as simple day: meal template"""
        if not plan or not plan.days:
            return "No meal plan available"
        
        output_lines = []
        
        for day_plan in plan.days:
            meal_desc = "No meal planned"
            
            if day_plan.dinner:
                meal_desc = day_plan.dinner.title
                if day_plan.dinner.cuisine_type:
                    meal_desc += f" ({day_plan.dinner.cuisine_type})"
            
            output_lines.append(f"{day_plan.day}: {meal_desc}")
        
        if plan.notes:
            output_lines.append(f"\nNotes: {plan.notes}")
        
        return "\n".join(output_lines)
    
    @staticmethod
    def to_markdown(plan: WeeklyMealPlan) -> str:
        """Format meal plan as markdown"""
        if not plan or not plan.days:
            return "# No meal plan available"
        
        output_lines = []
        output_lines.append("# 🍽️ Weekly Meal Plan")
        output_lines.append(f"**Week starting:** {plan.week_starting.strftime('%B %d, %Y')}")
        output_lines.append("")
        
        for day_plan in plan.days:
            output_lines.append(f"## {day_plan.day}")
            
            if day_plan.breakfast:
                output_lines.append(f"- **Breakfast:** {day_plan.breakfast.title}")
            
            if day_plan.lunch:
                output_lines.append(f"- **Lunch:** {day_plan.lunch.title}")
            
            if day_plan.dinner:
                dinner_line = f"- **Dinner:** {day_plan.dinner.title}"
                if day_plan.dinner.cuisine_type:
                    dinner_line += f" _{day_plan.dinner.cuisine_type}_"
                output_lines.append(dinner_line)
                
                if day_plan.dinner.prep_time:
                    output_lines.append(f"  - Prep time: {day_plan.dinner.prep_time} minutes")
            
            if day_plan.snacks:
                snack_names = [snack.title for snack in day_plan.snacks]
                output_lines.append(f"- **Snacks:** {', '.join(snack_names)}")
            
            if not any([day_plan.breakfast, day_plan.lunch, day_plan.dinner, day_plan.snacks]):
                output_lines.append("- *No meals planned*")
            
            output_lines.append("")
        
        if plan.notes:
            output_lines.append("## 📝 Notes")
            output_lines.append(plan.notes)
            output_lines.append("")
        
        if plan.grocery_list:
            output_lines.append("## 🛒 Grocery List")
            for item in plan.grocery_list:
                output_lines.append(f"- {item}")
        
        return "\n".join(output_lines)