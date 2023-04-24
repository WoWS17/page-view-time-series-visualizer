import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
df = df[(df['value'] > df['value'].quantile(0.025)) & (df['value'] < df['value'].quantile(0.975))]


# daily distribution of the number of pages viewed
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(80, 20))

    ax.plot(df.index, df['value'])
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    fig.savefig('line_plot.png')
    return fig

# Average daily page views for each month grouped by year.
def draw_bar_plot(): 
    fig, ax = plt.subplots(figsize=(16, 8))

    # Copy and modify data for monthly bar plot
    df['year'] = df.index.year
    df['month'] = df.index.month
    df_bar = df.groupby([df['year'], df['month']]).mean()

    df_pivot = df_bar.pivot_table(index='year', columns='month', values='value')

    # Create the bar plot
    df_pivot.plot(kind='bar', ax=ax)

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')

    ax.legend(title='Months', loc='upper left', 
              labels=['January', 'February', 'March', 'April', 'May', 'June', 'July',
                        'August', 'September', 'October', 'November', 'December'])

    fig.savefig('bar_plot.png')
    return fig

# These box plots shows how the values are distributed within a given year or month and how it compares over time.
def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
 
    fig, _ = plt.subplots(1, 2, figsize=(25,8))

    # Drawing first plot
    plt.subplot(1,2,1)
    sns.boxplot(x=df_box['year'], y=df_box['value'], data=df_box)

    plt.title('Year-wise Box Plot (Trend)')
    plt.xlabel('Year')
    plt.ylabel('Page Views')

    # Drawing second plot
    plt.subplot(1,2,2)
    sns.boxplot(x=df_box['month'], y=df_box['value'], data=df_box,
                         order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                        'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    plt.title('Month-wise Box Plot (Seasonality)')
    plt.xlabel('Month')
    plt.ylabel('Page Views')
    

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
