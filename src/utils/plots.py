import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_mission_trend(df: pd.DataFrame) -> go.Figure:
    """Erstellt den Haupt-Trendplot: Tägliche Einsätze vs. 7-Tage-Durchschnitt."""
    fig = px.line(
        df, 
        x='mission_date', 
        y=['total_missions', 'total_missions_7d_avg'],
        title='<b>Tägliche Notfalleinsätze & 7-Tage-Trend</b>',
        labels={'value': 'Anzahl Einsätze', 'mission_date': 'Datum', 'variable': 'Metrik'},
        color_discrete_map={'total_missions': '#94a3b8', 'total_missions_7d_avg': '#2563eb'}
    )
    
    # Linien-Styling anpassen
    fig.update_traces(selector=dict(name='total_missions'), line=dict(width=1, dash='dot'))
    fig.update_traces(selector=dict(name='total_missions_7d_avg'), line=dict(width=2.5))
    
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        legend=dict(title='', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def plot_mission_breakdown(df: pd.DataFrame) -> go.Figure:
    """Erstellt den Stacked Area Chart für Rettungsdienst vs. Feuerwehr."""
    fig = px.area(
        df, 
        x='mission_date', 
        y=['rescue_missions', 'fire_missions'],
        title='<b>Einsatzverteilung: Rettungsdienst vs. Feuerwehr</b>',
        labels={'value': 'Anzahl Einsätze', 'mission_date': 'Datum', 'variable': 'Einsatzart'},
        color_discrete_map={'rescue_missions': '#0284c7', 'fire_missions': '#dc2626'}
    )
    
    # Labels für Legende verschönern
    fig.for_each_trace(lambda t: t.update(name="Rettungsdienst" if t.name=="rescue_missions" else "Feuerwehr"))
    
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        legend=dict(title='', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def plot_weekday_distribution(df: pd.DataFrame) -> go.Figure:
    """Erstellt einen Boxplot für den Wochentagsvergleich (inkl. Wochenend-Highlight)."""
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    fig = px.box(
        df, 
        x='day_of_week', 
        y='total_missions',
        category_orders={'day_of_week': days_order},
        title='<b>Einsatzverteilung nach Wochentagen</b>',
        labels={'day_of_week': 'Wochentag', 'total_missions': 'Gesamteinsätze'},
        color='is_weekend',
        color_discrete_map={True: '#f59e0b', False: '#3b82f6'}
    )
    
    fig.update_layout(
        template='plotly_white',
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def plot_response_time(df: pd.DataFrame) -> go.Figure:
    """Erstellt den Trend der Median-Antwortzeit."""
    fig = px.line(
        df, 
        x='mission_date', 
        y='median_response_time_seconds',
        title='<b>Entwicklung der Median-Antwortzeit (Sekunden)</b>',
        labels={'median_response_time_seconds': 'Sekunden', 'mission_date': 'Datum'}
    )
    
    fig.update_traces(line=dict(color='#0d9488', width=2))
    
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig