# visuals.py
import matplotlib.pyplot as plt
import seaborn as sns

def plot_heatmap(df):
    """
    Plots a heatmap of task RiskScores.
    """
    plt.figure(figsize=(10, 4))
    sns.heatmap(df[['RiskScore']].T, annot=True, cmap="YlOrRd", cbar=True)
    plt.title("Task Risk Heatmap")
    return plt.gcf()

def plot_top_risk_tasks(df, top_n=5):
    """
    Plots horizontal bar chart of top N risky tasks.
    """
    top_tasks = df.sort_values(by='RiskScore', ascending=False).head(top_n)
    plt.figure(figsize=(10, 5))
    sns.barplot(
        x='RiskScore',
        y='TaskName',
        data=top_tasks,
        palette="Reds_r"
    )
    plt.title(f"Top {top_n} Risky Tasks")
    plt.xlabel("Risk Score")
    plt.ylabel("Task Name")
    plt.xlim(0, 1)
    plt.tight_layout()
    return plt.gcf()