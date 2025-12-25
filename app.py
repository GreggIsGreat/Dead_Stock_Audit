import dash
from dash import dcc, html, dash_table, callback_context
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import base64
import io
from datetime import datetime

# Initialize app with external stylesheets
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ]
)
server = app.server

# Professional color palette
COLORS = {
    # Status colors
    'dead': '#dc3545',
    'slow': '#fd7e14',
    'moderate': '#0dcaf0',
    'active': '#198754',
    
    # UI colors
    'primary': '#0d6efd',
    'secondary': '#6c757d',
    'dark': '#212529',
    'light': '#f8f9fa',
    'white': '#ffffff',
    
    # Backgrounds
    'bg_primary': '#0f172a',
    'bg_secondary': '#1e293b',
    'bg_card': '#ffffff',
    'bg_page': '#f1f5f9',
    
    # Accents
    'accent': '#3b82f6',
    'accent_light': '#60a5fa',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    
    # Text
    'text_primary': '#1e293b',
    'text_secondary': '#64748b',
    'text_muted': '#94a3b8',
    'text_white': '#ffffff',
    
    # Borders
    'border': '#e2e8f0',
    'border_light': '#f1f5f9'
}

STATUS_COLORS = {
    'Dead Stock (6+ months)': COLORS['dead'],
    'Slow Moving (3-6 months)': COLORS['slow'],
    'Moderate (1-3 months)': COLORS['moderate'],
    'Active (< 1 month)': COLORS['active']
}

# Reusable styles
CARD_STYLE = {
    'background': COLORS['white'],
    'borderRadius': '16px',
    'boxShadow': '0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.05)',
    'border': f'1px solid {COLORS["border_light"]}',
    'overflow': 'hidden'
}

SECTION_HEADER_STYLE = {
    'fontSize': '18px',
    'fontWeight': '600',
    'color': COLORS['text_primary'],
    'marginBottom': '20px',
    'display': 'flex',
    'alignItems': 'center',
    'gap': '10px'
}

# App layout
app.layout = html.Div([
    # Navigation Bar
    html.Nav([
        html.Div([
            # Logo and brand
            html.Div([
                html.Div([
                    html.Span("📦", style={'fontSize': '24px'})
                ], style={
                    'width': '44px',
                    'height': '44px',
                    'background': 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
                    'borderRadius': '12px',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center'
                }),
                html.Div([
                    html.H1("StockAudit", style={
                        'margin': '0',
                        'fontSize': '20px',
                        'fontWeight': '700',
                        'color': COLORS['text_white']
                    }),
                    html.Span("Spaza Shop Edition", style={
                        'fontSize': '11px',
                        'color': COLORS['text_muted'],
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.5px'
                    })
                ])
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '12px'}),
            
            # Right side - Botswana flag indicator
            html.Div([
                html.Div([
                    html.Span("🇧🇼", style={'fontSize': '20px'}),
                    html.Span("BWP", style={
                        'fontSize': '12px',
                        'fontWeight': '600',
                        'color': COLORS['text_muted']
                    })
                ], style={'display': 'flex', 'alignItems': 'center', 'gap': '6px'})
            ])
        ], style={
            'maxWidth': '1400px',
            'margin': '0 auto',
            'padding': '0 24px',
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'height': '70px'
        })
    ], style={
        'background': COLORS['bg_primary'],
        'borderBottom': f'1px solid {COLORS["bg_secondary"]}',
        'position': 'sticky',
        'top': '0',
        'zIndex': '1000'
    }),
    
    # Main content wrapper
    html.Div([
        # Hero Upload Section
        html.Div([
            html.Div([
                # Left side - Info
                html.Div([
                    html.Div([
                        html.Span("NEW", style={
                            'background': COLORS['success'],
                            'color': 'white',
                            'padding': '4px 10px',
                            'borderRadius': '20px',
                            'fontSize': '10px',
                            'fontWeight': '700',
                            'letterSpacing': '0.5px'
                        })
                    ], style={'marginBottom': '16px'}),
                    
                    html.H2("Identify Dead Stock Instantly", style={
                        'fontSize': '32px',
                        'fontWeight': '700',
                        'color': COLORS['text_primary'],
                        'marginBottom': '12px',
                        'lineHeight': '1.2'
                    }),
                    
                    html.P(
                        "Upload your inventory data and discover how much cash is trapped in slow-moving stock. "
                        "Get actionable insights to free up capital and grow your spaza shop.",
                        style={
                            'fontSize': '16px',
                            'color': COLORS['text_secondary'],
                            'lineHeight': '1.6',
                            'marginBottom': '24px'
                        }
                    ),
                    
                    # Feature bullets
                    html.Div([
                        html.Div([
                            html.Span("✓", style={
                                'color': COLORS['success'],
                                'fontWeight': '700',
                                'marginRight': '10px'
                            }),
                            "Automatic stock classification"
                        ], style={'marginBottom': '8px', 'color': COLORS['text_secondary']}),
                        html.Div([
                            html.Span("✓", style={
                                'color': COLORS['success'],
                                'fontWeight': '700',
                                'marginRight': '10px'
                            }),
                            "Holding cost calculation"
                        ], style={'marginBottom': '8px', 'color': COLORS['text_secondary']}),
                        html.Div([
                            html.Span("✓", style={
                                'color': COLORS['success'],
                                'fontWeight': '700',
                                'marginRight': '10px'
                            }),
                            "Priority action recommendations"
                        ], style={'color': COLORS['text_secondary']})
                    ])
                ], style={'flex': '1', 'paddingRight': '40px'}),
                
                # Right side - Upload card
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("📤", style={'fontSize': '32px', 'marginBottom': '12px', 'display': 'block'}),
                            html.P("Upload Inventory CSV", style={
                                'fontSize': '16px',
                                'fontWeight': '600',
                                'color': COLORS['text_primary'],
                                'marginBottom': '4px'
                            }),
                            html.P("Drag & drop or click to browse", style={
                                'fontSize': '13px',
                                'color': COLORS['text_muted'],
                                'margin': '0'
                            })
                        ], style={'textAlign': 'center'})
                    ], style={
                        'border': f'2px dashed {COLORS["border"]}',
                        'borderRadius': '12px',
                        'padding': '32px',
                        'cursor': 'pointer',
                        'transition': 'all 0.2s ease',
                        'marginBottom': '16px'
                    }),
                    
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            html.Span("📁 Choose File", style={'marginRight': '8px'}),
                        ]),
                        style={
                            'width': '100%',
                            'padding': '14px',
                            'background': COLORS['bg_page'],
                            'border': f'1px solid {COLORS["border"]}',
                            'borderRadius': '10px',
                            'textAlign': 'center',
                            'cursor': 'pointer',
                            'fontSize': '14px',
                            'fontWeight': '500',
                            'color': COLORS['text_secondary']
                        },
                        multiple=False
                    ),
                    
                    html.Div(id='upload-status', style={
                        'marginTop': '12px',
                        'textAlign': 'center',
                        'minHeight': '24px'
                    }),
                    
                    html.Div([
                        html.Div(style={
                            'height': '1px',
                            'background': COLORS['border'],
                            'flex': '1'
                        }),
                        html.Span("or", style={
                            'padding': '0 16px',
                            'color': COLORS['text_muted'],
                            'fontSize': '13px'
                        }),
                        html.Div(style={
                            'height': '1px',
                            'background': COLORS['border'],
                            'flex': '1'
                        })
                    ], style={
                        'display': 'flex',
                        'alignItems': 'center',
                        'margin': '20px 0'
                    }),
                    
                    html.Button([
                        html.Span("▶", style={'marginRight': '8px'}),
                        "Load Demo Data"
                    ], id='load-sample', style={
                        'width': '100%',
                        'padding': '14px 24px',
                        'background': 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '10px',
                        'fontSize': '14px',
                        'fontWeight': '600',
                        'cursor': 'pointer',
                        'boxShadow': '0 4px 14px rgba(59, 130, 246, 0.4)',
                        'transition': 'all 0.2s ease'
                    })
                ], style={
                    **CARD_STYLE,
                    'padding': '28px',
                    'width': '380px',
                    'flexShrink': '0'
                })
            ], style={
                'display': 'flex',
                'alignItems': 'center',
                'maxWidth': '1000px',
                'margin': '0 auto'
            })
        ], style={
            'padding': '60px 24px',
            'background': f'linear-gradient(180deg, {COLORS["bg_page"]} 0%, {COLORS["white"]} 100%)'
        }),
        
        # Data store
        dcc.Store(id='inventory-data'),
        
        # Dashboard content
        html.Div(id='dashboard-content', style={'display': 'none'})
        
    ], style={'minHeight': 'calc(100vh - 70px)'})
    
], style={
    'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    'background': COLORS['bg_page'],
    'minHeight': '100vh',
    'margin': '0'
})


# ============== HELPER FUNCTIONS ==============

def parse_contents(contents, filename):
    """Parse uploaded CSV"""
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        return df, None
    except Exception as e:
        return None, str(e)


def process_data(df):
    """Process and validate data"""
    required = ['sku', 'product_name', 'category', 'unit_cost', 'current_stock']
    missing = [c for c in required if c not in df.columns]
    
    if missing:
        return None, f"Missing columns: {', '.join(missing)}"
    
    if 'stock_value' not in df.columns:
        df['stock_value'] = df['current_stock'] * df['unit_cost']
    
    if 'stock_status' not in df.columns and 'days_since_last_sale' in df.columns:
        df['stock_status'] = df['days_since_last_sale'].apply(
            lambda x: 'Dead Stock (6+ months)' if x > 180 else
                      'Slow Moving (3-6 months)' if x > 90 else
                      'Moderate (1-3 months)' if x > 30 else
                      'Active (< 1 month)'
        )
    
    if 'urgency_score' not in df.columns:
        df['urgency_score'] = 50
    
    if 'holding_cost' not in df.columns:
        df['holding_cost'] = 0
        
    if 'action_required' not in df.columns:
        df['action_required'] = df['stock_status'].apply(
            lambda x: 'Clearance Sale' if x == 'Dead Stock (6+ months)' else
                      'Discount / Promote' if x == 'Slow Moving (3-6 months)' else
                      'Monitor' if x == 'Moderate (1-3 months)' else 'Restock'
        )
    
    if 'monthly_velocity' not in df.columns:
        df['monthly_velocity'] = 0
    
    return df, None


# ============== UI COMPONENTS ==============

def create_metric_card(icon, title, value, subtitle, trend=None, trend_up=True, color=None):
    """Create a professional metric card"""
    trend_color = COLORS['success'] if trend_up else COLORS['danger']
    
    return html.Div([
        html.Div([
            html.Div([
                html.Span(icon, style={'fontSize': '20px'})
            ], style={
                'width': '48px',
                'height': '48px',
                'background': f'{color}15' if color else COLORS['bg_page'],
                'borderRadius': '12px',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center',
                'marginBottom': '16px'
            }),
            html.P(title, style={
                'fontSize': '13px',
                'color': COLORS['text_muted'],
                'margin': '0 0 8px 0',
                'fontWeight': '500',
                'textTransform': 'uppercase',
                'letterSpacing': '0.5px'
            }),
            html.H3(value, style={
                'fontSize': '28px',
                'fontWeight': '700',
                'color': color if color else COLORS['text_primary'],
                'margin': '0 0 4px 0',
                'letterSpacing': '-0.5px'
            }),
            html.Div([
                html.Span(subtitle, style={
                    'fontSize': '13px',
                    'color': COLORS['text_secondary']
                }),
                html.Span([
                    html.Span("↑ " if trend_up else "↓ ", style={'fontSize': '11px'}),
                    trend
                ], style={
                    'fontSize': '12px',
                    'color': trend_color,
                    'fontWeight': '600',
                    'marginLeft': '8px'
                }) if trend else None
            ], style={'display': 'flex', 'alignItems': 'center'})
        ])
    ], style={
        **CARD_STYLE,
        'padding': '24px'
    })


def create_kpi_section(df):
    """Create KPI cards section"""
    dead = df[df['stock_status'] == 'Dead Stock (6+ months)']
    slow = df[df['stock_status'] == 'Slow Moving (3-6 months)']
    active = df[df['stock_status'] == 'Active (< 1 month)']
    
    total_value = df['stock_value'].sum()
    dead_value = dead['stock_value'].sum()
    slow_value = slow['stock_value'].sum()
    holding_cost = df['holding_cost'].sum()
    problem_pct = ((len(dead) + len(slow)) / len(df)) * 100 if len(df) > 0 else 0
    
    return html.Div([
        create_metric_card(
            "💀", "Dead Stock Value",
            f"P{dead_value:,.0f}",
            f"{len(dead)} products",
            color=COLORS['danger']
        ),
        create_metric_card(
            "🐌", "Slow Moving",
            f"P{slow_value:,.0f}",
            f"{len(slow)} products",
            color=COLORS['warning']
        ),
        create_metric_card(
            "💸", "Holding Costs",
            f"P{holding_cost:,.0f}",
            "Accumulated waste",
            color=COLORS['accent']
        ),
        create_metric_card(
            "📊", "Problem Rate",
            f"{problem_pct:.1f}%",
            f"of {len(df)} total items",
            color=COLORS['secondary']
        ),
        create_metric_card(
            "✅", "Healthy Stock",
            f"P{active['stock_value'].sum():,.0f}",
            f"{len(active)} active items",
            color=COLORS['success']
        ),
        create_metric_card(
            "💰", "Total Inventory",
            f"P{total_value:,.0f}",
            f"{df['current_stock'].sum():,.0f} units",
            color=COLORS['text_primary']
        )
    ], style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))',
        'gap': '20px',
        'marginBottom': '32px'
    })


# ============== CHART FUNCTIONS ==============

def create_status_chart(df):
    """Professional donut chart"""
    summary = df.groupby('stock_status')['stock_value'].sum().reset_index()
    
    fig = go.Figure(data=[go.Pie(
        labels=summary['stock_status'],
        values=summary['stock_value'],
        hole=0.65,
        marker=dict(
            colors=[STATUS_COLORS.get(s, COLORS['secondary']) for s in summary['stock_status']],
            line=dict(color=COLORS['white'], width=3)
        ),
        textinfo='percent',
        textposition='outside',
        textfont=dict(size=12, color=COLORS['text_secondary']),
        hovertemplate="<b>%{label}</b><br>P%{value:,.0f}<br>%{percent}<extra></extra>"
    )])
    
    # Add center text
    total_value = df['stock_value'].sum()
    fig.add_annotation(
        text=f"<b>P{total_value:,.0f}</b>",
        x=0.5, y=0.55,
        font=dict(size=20, color=COLORS['text_primary']),
        showarrow=False
    )
    fig.add_annotation(
        text="Total Value",
        x=0.5, y=0.42,
        font=dict(size=11, color=COLORS['text_muted']),
        showarrow=False
    )
    
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color=COLORS['text_secondary'])
        ),
        margin=dict(t=20, b=60, l=20, r=20),
        height=320,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_category_chart(df):
    """Professional horizontal bar chart"""
    problem = df[df['stock_status'].isin(['Dead Stock (6+ months)', 'Slow Moving (3-6 months)'])]
    
    if len(problem) == 0:
        # Return empty chart if no problem stock
        fig = go.Figure()
        fig.add_annotation(
            text="No problem stock found! 🎉",
            x=0.5, y=0.5,
            font=dict(size=16, color=COLORS['success']),
            showarrow=False,
            xref="paper", yref="paper"
        )
        fig.update_layout(
            height=320,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return fig
    
    cat_summary = problem.groupby('category')['stock_value'].sum().sort_values(ascending=True).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=cat_summary['category'],
        x=cat_summary['stock_value'],
        orientation='h',
        marker=dict(
            color=cat_summary['stock_value'],
            colorscale=[[0, COLORS['warning']], [1, COLORS['danger']]],
            line=dict(width=0)
        ),
        hovertemplate="<b>%{y}</b><br>P%{x:,.0f}<extra></extra>"
    ))
    
    fig.update_layout(
        xaxis_title="Stock Value (Pula)",
        yaxis_title="",
        font=dict(family="Segoe UI", size=12, color=COLORS['text_secondary']),
        margin=dict(t=20, b=50, l=120, r=30),
        height=320,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            gridcolor=COLORS['border_light'],
            zerolinecolor=COLORS['border']
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0)'
        ),
        bargap=0.3
    )
    
    return fig


def create_aging_chart(df):
    """Professional scatter plot"""
    fig = px.scatter(
        df,
        x='days_since_last_sale',
        y='stock_value',
        color='stock_status',
        color_discrete_map=STATUS_COLORS,
        size='current_stock',
        size_max=30,
        hover_name='product_name',
        hover_data={
            'category': True,
            'days_since_last_sale': True,
            'stock_value': ':.2f',
            'stock_status': False,
            'current_stock': True
        }
    )
    
    # Add danger zone
    max_days = df['days_since_last_sale'].max() if len(df) > 0 else 200
    fig.add_vrect(
        x0=180, x1=max_days + 20,
        fillcolor=COLORS['danger'], opacity=0.08,
        line_width=0
    )
    
    fig.add_vline(
        x=180,
        line_dash="dash",
        line_color=COLORS['danger'],
        line_width=2,
        annotation_text="Dead Stock Zone",
        annotation_position="top",
        annotation_font=dict(size=11, color=COLORS['danger'])
    )
    
    fig.update_traces(
        marker=dict(
            line=dict(width=1, color=COLORS['white']),
            opacity=0.8
        )
    )
    
    fig.update_layout(
        xaxis_title="Days Since Last Sale",
        yaxis_title="Stock Value (Pula)",
        font=dict(family="Segoe UI", size=12, color=COLORS['text_secondary']),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            title="",
            font=dict(size=11)
        ),
        margin=dict(t=30, b=80, l=70, r=30),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor=COLORS['border_light'], zerolinecolor=COLORS['border']),
        yaxis=dict(gridcolor=COLORS['border_light'], zerolinecolor=COLORS['border'])
    )
    
    return fig


def create_velocity_histogram(df):
    """Monthly velocity distribution chart"""
    fig = go.Figure()
    
    status_order = [
        'Active (< 1 month)',
        'Moderate (1-3 months)',
        'Slow Moving (3-6 months)',
        'Dead Stock (6+ months)'
    ]
    
    for status in status_order:
        data = df[df['stock_status'] == status]['monthly_velocity']
        if len(data) > 0:
            fig.add_trace(go.Histogram(
                x=data,
                name=status.split('(')[0].strip(),
                marker=dict(
                    color=STATUS_COLORS[status],
                    line=dict(width=1, color='white')
                ),
                opacity=0.75,
                nbinsx=20
            ))
    
    fig.update_layout(
        barmode='overlay',
        xaxis_title="Units Sold per Month",
        yaxis_title="Number of Products",
        font=dict(family="Segoe UI", size=12, color=COLORS['text_secondary']),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        ),
        margin=dict(t=20, b=80, l=60, r=30),
        height=320,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor=COLORS['border_light']),
        yaxis=dict(gridcolor=COLORS['border_light'])
    )
    
    return fig


# ============== TABLE COMPONENTS ==============

def create_priority_table(df):
    """Professional data table"""
    priority = df.nlargest(10, 'urgency_score')[[
        'sku', 'product_name', 'category', 'current_stock',
        'stock_value', 'days_since_last_sale', 'urgency_score', 'action_required'
    ]].copy()
    
    return dash_table.DataTable(
        data=priority.to_dict('records'),
        columns=[
            {'name': 'SKU', 'id': 'sku'},
            {'name': 'Product', 'id': 'product_name'},
            {'name': 'Category', 'id': 'category'},
            {'name': 'Stock', 'id': 'current_stock', 'type': 'numeric'},
            {'name': 'Value (P)', 'id': 'stock_value', 'type': 'numeric', 'format': {'specifier': ',.2f'}},
            {'name': 'Days Idle', 'id': 'days_since_last_sale', 'type': 'numeric'},
            {'name': 'Priority', 'id': 'urgency_score', 'type': 'numeric'},
            {'name': 'Action', 'id': 'action_required'}
        ],
        style_table={
            'overflowX': 'auto',
            'borderRadius': '12px'
        },
        style_cell={
            'textAlign': 'left',
            'padding': '16px 20px',
            'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
            'fontSize': '13px',
            'color': COLORS['text_primary'],
            'border': 'none',
            'borderBottom': f'1px solid {COLORS["border_light"]}'
        },
        style_header={
            'backgroundColor': COLORS['bg_page'],
            'fontWeight': '600',
            'fontSize': '11px',
            'color': COLORS['text_muted'],
            'textTransform': 'uppercase',
            'letterSpacing': '0.5px',
            'border': 'none',
            'borderBottom': f'2px solid {COLORS["border"]}'
        },
        style_data_conditional=[
            {
                'if': {'filter_query': '{urgency_score} >= 75'},
                'backgroundColor': '#fef2f2'
            },
            {
                'if': {'filter_query': '{urgency_score} >= 50 && {urgency_score} < 75'},
                'backgroundColor': '#fffbeb'
            },
            {
                'if': {'column_id': 'action_required'},
                'fontWeight': '600',
                'color': COLORS['accent']
            },
            {
                'if': {'column_id': 'urgency_score'},
                'fontWeight': '700'
            },
            {
                'if': {'state': 'active'},
                'backgroundColor': COLORS['bg_page'],
                'border': 'none'
            }
        ],
        page_size=10,
        sort_action='native',
        filter_action='native',
        style_as_list_view=True
    )


# ============== ACTION CARDS ==============

def create_action_cards(df):
    """Create actionable insight cards"""
    dead = df[df['stock_status'] == 'Dead Stock (6+ months)']
    dead_value = dead['stock_value'].sum()
    
    if len(dead) > 0:
        top_dead_cat = dead.groupby('category')['stock_value'].sum().idxmax()
        top_dead_val = dead.groupby('category')['stock_value'].sum().max()
    else:
        top_dead_cat = "N/A"
        top_dead_val = 0
    
    at_risk = df[(df['days_since_last_sale'] > 60) & (df['days_since_last_sale'] <= 90)]
    
    actions = [
        {
            "icon": "🚨",
            "title": "Immediate: Clear Dead Stock",
            "description": f"P{dead_value:,.0f} trapped in {len(dead)} dead items. Run a clearance sale this weekend.",
            "action": "Start Clearance",
            "color": COLORS['danger']
        },
        {
            "icon": "📦",
            "title": f"Focus: {top_dead_cat}",
            "description": f"This category has P{top_dead_val:,.0f} stuck. Review supplier minimum orders.",
            "action": "Review Category",
            "color": COLORS['warning']
        },
        {
            "icon": "⏰",
            "title": f"At Risk: {len(at_risk)} Items",
            "description": f"P{at_risk['stock_value'].sum():,.0f} becoming dead soon. Promote on WhatsApp.",
            "action": "Create Promo",
            "color": COLORS['accent']
        },
        {
            "icon": "💡",
            "title": "Quick Win",
            "description": f"Selling 50% of dead stock at cost frees P{dead_value*0.5:,.0f} for fast sellers.",
            "action": "Calculate ROI",
            "color": COLORS['success']
        }
    ]
    
    cards = []
    for action in actions:
        cards.append(
            html.Div([
                html.Div([
                    html.Span(action['icon'], style={'fontSize': '24px'}),
                ], style={
                    'width': '48px',
                    'height': '48px',
                    'background': f'{action["color"]}15',
                    'borderRadius': '12px',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'marginBottom': '16px'
                }),
                html.H4(action['title'], style={
                    'fontSize': '15px',
                    'fontWeight': '600',
                    'color': COLORS['text_primary'],
                    'margin': '0 0 8px 0'
                }),
                html.P(action['description'], style={
                    'fontSize': '13px',
                    'color': COLORS['text_secondary'],
                    'lineHeight': '1.5',
                    'margin': '0 0 16px 0'
                }),
                html.Button(action['action'], style={
                    'background': 'transparent',
                    'border': f'1px solid {action["color"]}',
                    'color': action['color'],
                    'padding': '8px 16px',
                    'borderRadius': '8px',
                    'fontSize': '12px',
                    'fontWeight': '600',
                    'cursor': 'pointer'
                })
            ], style={
                **CARD_STYLE,
                'padding': '24px'
            })
        )
    
    return html.Div(cards, style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(260px, 1fr))',
        'gap': '20px'
    })


# ============== SUMMARY BANNER ==============

def create_summary_banner(df):
    """Create summary banner at top of dashboard"""
    dead = df[df['stock_status'] == 'Dead Stock (6+ months)']
    dead_value = dead['stock_value'].sum()
    total_value = df['stock_value'].sum()
    dead_pct = (dead_value / total_value * 100) if total_value > 0 else 0
    
    return html.Div([
        html.Div([
            html.Div([
                html.Span("📊", style={'fontSize': '24px', 'marginRight': '12px'}),
                html.Div([
                    html.Span("Analysis Complete", style={
                        'fontSize': '12px',
                        'color': COLORS['text_muted'],
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.5px'
                    }),
                    html.H3(f"P{dead_value:,.0f} Found in Dead Stock", style={
                        'margin': '4px 0 0 0',
                        'fontSize': '20px',
                        'fontWeight': '700',
                        'color': COLORS['text_primary']
                    })
                ])
            ], style={'display': 'flex', 'alignItems': 'center'}),
            
            html.Div([
                html.Div([
                    html.Span(f"{dead_pct:.1f}%", style={
                        'fontSize': '24px',
                        'fontWeight': '700',
                        'color': COLORS['danger']
                    }),
                    html.Span(" of inventory value is stuck", style={
                        'color': COLORS['text_secondary'],
                        'marginLeft': '8px'
                    })
                ])
            ])
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'flexWrap': 'wrap',
            'gap': '20px'
        })
    ], style={
        **CARD_STYLE,
        'padding': '24px 32px',
        'marginBottom': '32px',
        'borderLeft': f'4px solid {COLORS["danger"]}'
    })


# ============== MAIN CALLBACK ==============

@app.callback(
    [Output('inventory-data', 'data'),
     Output('upload-status', 'children'),
     Output('dashboard-content', 'style'),
     Output('dashboard-content', 'children')],
    [Input('upload-data', 'contents'),
     Input('load-sample', 'n_clicks')],
    [State('upload-data', 'filename')]
)
def update_dashboard(contents, n_clicks, filename):
    ctx = callback_context
    
    if not ctx.triggered:
        return None, "", {'display': 'none'}, None
    
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger == 'load-sample' and n_clicks:
        from generate_data import generate_spaza_inventory
        df = generate_spaza_inventory()
        status = html.Div([
            html.Span("✓", style={
                'color': COLORS['success'],
                'fontWeight': 'bold',
                'marginRight': '8px'
            }),
            "Demo data loaded successfully"
        ], style={'color': COLORS['success'], 'fontSize': '13px'})
    
    elif trigger == 'upload-data' and contents:
        df, error = parse_contents(contents, filename)
        if error:
            return None, html.Div([
                html.Span("✗", style={'color': COLORS['danger'], 'marginRight': '8px'}),
                f"Error: {error}"
            ], style={'color': COLORS['danger'], 'fontSize': '13px'}), {'display': 'none'}, None
        
        df, error = process_data(df)
        if error:
            return None, html.Div([
                html.Span("✗", style={'color': COLORS['danger'], 'marginRight': '8px'}),
                error
            ], style={'color': COLORS['danger'], 'fontSize': '13px'}), {'display': 'none'}, None
        
        status = html.Div([
            html.Span("✓", style={
                'color': COLORS['success'],
                'fontWeight': 'bold',
                'marginRight': '8px'
            }),
            f"Loaded {len(df)} products from {filename}"
        ], style={'color': COLORS['success'], 'fontSize': '13px'})
    else:
        return None, "", {'display': 'none'}, None
    
    # Build dashboard
    dashboard = html.Div([
        # Main container
        html.Div([
            # Summary Banner
            create_summary_banner(df),
            
            # KPI Cards
            create_kpi_section(df),
            
            # Charts Row 1
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("📈", style={'marginRight': '8px'}),
                        "Stock Value Distribution"
                    ], style=SECTION_HEADER_STYLE),
                    dcc.Graph(
                        figure=create_status_chart(df),
                        config={'displayModeBar': False}
                    )
                ], style={**CARD_STYLE, 'padding': '24px'}),
                
                html.Div([
                    html.Div([
                        html.Span("📦", style={'marginRight': '8px'}),
                        "Problem Stock by Category"
                    ], style=SECTION_HEADER_STYLE),
                    dcc.Graph(
                        figure=create_category_chart(df),
                        config={'displayModeBar': False}
                    )
                ], style={**CARD_STYLE, 'padding': '24px'})
            ], style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(400px, 1fr))',
                'gap': '24px',
                'marginBottom': '24px'
            }),
            
            # Aging Analysis Chart
            html.Div([
                html.Div([
                    html.Span("📅", style={'marginRight': '8px'}),
                    "Stock Aging Analysis"
                ], style=SECTION_HEADER_STYLE),
                dcc.Graph(
                    figure=create_aging_chart(df),
                    config={'displayModeBar': False}
                )
            ], style={**CARD_STYLE, 'padding': '24px', 'marginBottom': '24px'}),
            
            # Velocity Chart
            html.Div([
                html.Div([
                    html.Span("⚡", style={'marginRight': '8px'}),
                    "Inventory Velocity"
                ], style=SECTION_HEADER_STYLE),
                dcc.Graph(
                    figure=create_velocity_histogram(df),
                    config={'displayModeBar': False}
                )
            ], style={**CARD_STYLE, 'padding': '24px', 'marginBottom': '24px'}),
            
            # Priority Table
            html.Div([
                html.Div([
                    html.Span("🎯", style={'marginRight': '8px'}),
                    "Priority Action Items"
                ], style=SECTION_HEADER_STYLE),
                create_priority_table(df)
            ], style={**CARD_STYLE, 'padding': '24px', 'marginBottom': '24px'}),
            
            # Action Cards
            html.Div([
                html.Div([
                    html.Span("💡", style={'marginRight': '8px'}),
                    "Recommended Actions"
                ], style=SECTION_HEADER_STYLE),
                create_action_cards(df)
            ], style={'marginBottom': '32px'}),
            
            # Footer
            html.Div([
                html.Div([
                    html.Span("📦 StockAudit", style={
                        'fontWeight': '600',
                        'color': COLORS['text_primary']
                    }),
                    html.Span(" • ", style={'color': COLORS['text_muted']}),
                    html.Span("Spaza Shop Edition", style={'color': COLORS['text_muted']}),
                    html.Span(" • ", style={'color': COLORS['text_muted']}),
                    html.Span("Made for Botswana 🇧🇼", style={'color': COLORS['text_muted']})
                ])
            ], style={
                'textAlign': 'center',
                'padding': '24px',
                'borderTop': f'1px solid {COLORS["border"]}',
                'fontSize': '13px'
            })
            
        ], style={
            'maxWidth': '1400px',
            'margin': '0 auto',
            'padding': '32px 24px'
        })
    ], style={
        'background': COLORS['bg_page']
    })
    
    return df.to_json(), status, {'display': 'block'}, dashboard


# ============== RUN SERVER ==============

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)