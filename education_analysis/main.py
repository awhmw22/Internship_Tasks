# --- Importing necessary libraries ---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# PDF report generation libraries
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# --- Load the dataset ---
df = pd.read_csv(r'data\student-por.csv', sep=';')

# --- Add a calculated final grade percentage column ---
df['final_grade'] = (df['G3'] / 20) * 100

# --- Set visualization style ---
sns.set_style("whitegrid")

# --- Creating a folder for saving visualizations ---
os.makedirs("visualizations", exist_ok=True)

# --- Plot 1: Boxplot - Study Time vs Final Grades ---
plt.figure(figsize=(10, 6))
sns.boxplot(x='studytime', y='final_grade', data=df)
plt.title('Final Grades vs. Weekly Study Time', fontsize=16)
plt.xlabel('Weekly Study Time (1: <2 hrs, 2: 2-5 hrs, 3: 5-10 hrs, 4: >10 hrs)', fontsize=12)
plt.ylabel('Final Grade (in %)', fontsize=12)
plt.tight_layout()
plt.savefig("visualizations/studytime_vs_grade.png")
plt.close()

# --- Plot 2: Violin plot - Family Support vs Final Grades ---
plt.figure(figsize=(8, 6))
sns.violinplot(x='famsup', y='final_grade', data=df)
plt.title('Impact of Family Educational Support on Final Grades', fontsize=16)
plt.xlabel('Family Educational Support', fontsize=12)
plt.ylabel('Final Grade (in %)', fontsize=12)
plt.tight_layout()
plt.savefig("visualizations/famsup_vs_grade.png")
plt.close()

# --- Plot 3: Barplot - Going Out vs Final Grades ---
plt.figure(figsize=(10, 6))
sns.barplot(x='goout', y='final_grade', data=df, palette='viridis', hue='goout', legend=False)
plt.title('Average Final Grade vs. Going Out Frequency', fontsize=16)
plt.xlabel('Frequency of Going Out (1: Very Low - 5: Very High)', fontsize=12)
plt.ylabel('Average Final Grade (in %)', fontsize=12)
plt.tight_layout()
plt.savefig("visualizations/goout_vs_grade.png")
plt.close()

# --- Generating PDF Report ---
doc = SimpleDocTemplate("Student_Performance_Analysis_Report.pdf", pagesize=A4)
styles = getSampleStyleSheet()
story = []

# Title
story.append(Paragraph("📊 Student Performance Analysis Report", styles['Title']))
story.append(Spacer(1, 12))

# Introduction
intro_text = """
This report explores the relationship between student behavior and academic performance using the UCI Student Performance dataset.
I analyzed how weekly study time, family support, and social activity impact final grades (converted to percentage).
The data was visualized using Seaborn and Matplotlib in Python.
"""
story.append(Paragraph(intro_text, styles['BodyText']))
story.append(Spacer(1, 12))

# Visualization 1
story.append(Paragraph("1️⃣ Final Grades vs Weekly Study Time", styles['Heading2']))
story.append(Image("visualizations/studytime_vs_grade.png", width=5*inch, height=3*inch))
story.append(Spacer(1, 12))
story.append(Paragraph("""
This box plot shows how study time correlates with final grades. Students who study more tend to score higher, 
with noticeable improvement in the 3rd and 4th study categories (5–10 hours and more than 10 hours weekly).
""", styles['BodyText']))
story.append(Spacer(1, 12))

# Visualization 2
story.append(Paragraph("2️⃣ Impact of Family Educational Support on Grades", styles['Heading2']))
story.append(Image("visualizations/famsup_vs_grade.png", width=5*inch, height=3*inch))
story.append(Spacer(1, 12))
story.append(Paragraph("""
This violin plot highlights that students who receive family educational support generally perform better. 
The grade distribution is higher for students who answered 'yes' to receiving family support.
""", styles['BodyText']))
story.append(Spacer(1, 12))

# Visualization 3
story.append(Paragraph("3️⃣ Social Activity vs Final Grades", styles['Heading2']))
story.append(Image("visualizations/goout_vs_grade.png", width=5*inch, height=3*inch))
story.append(Spacer(1, 12))
story.append(Paragraph("""
This bar plot suggests that students who go out more frequently tend to score slightly lower on average. 
There’s a visible decline in grades from low to high going-out frequencies.
""", styles['BodyText']))
story.append(Spacer(1, 24))

# Conclusion
story.append(Paragraph("✅ Conclusion", styles['Heading2']))
story.append(Paragraph("""
Academic performance is strongly influenced by factors like study time, parental support, and social activity.
This kind of analysis can help schools and educators target support strategies for different student behaviors.
""", styles['BodyText']))

# Building the PDF
doc.build(story)
