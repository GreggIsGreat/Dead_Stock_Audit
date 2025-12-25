import dash
from dash import dcc, html, dash_table, callback_context
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import base64
import io
from datetime import datetime, timedelta
import random

# ============== DATA GENERATOR (EMBEDDED) ==============

def generate_spaza_inventory(num_products=120, seed=42):
    """Generate realistic Spaza Shop inventory data for Botswana"""
    
    np.random.seed(seed)
    random.seed(seed)
    
    categories = {
        'Groceries': {
            'price_range': (8, 120),
            'holding_cost_pct': 0.02,
            'seasonality': [12, 1, 4],
            'products': [
                ('Maize Meal 2.5kg', 'White Star'),
                ('Maize Meal 5kg', 'White Star'),
                ('Cooking Oil 750ml', 'Sunfoil'),
                ('Cooking Oil 2L', 'Golden Fry'),
                ('Sugar 2kg', 'White'),
                ('Sugar 1kg', 'Brown'),
                ('Rice 2kg', 'Tastic'),
                ('Flour 2.5kg', 'Snowflake'),
                ('Salt 500g', 'Cerebos'),
                ('Tea 100 bags', 'Five Roses'),
                ('Coffee 200g', 'Ricoffy'),
                ('Beans 410g', 'KOO'),
                ('Pilchards 400g', 'Lucky Star'),
                ('Tomato Sauce 700ml', 'All Gold'),
                ('Peanut Butter 400g', 'Black Cat'),
            ]
        },
        'Beverages': {
            'price_range': (5, 35),
            'holding_cost_pct': 0.015,
            'seasonality': [10, 11, 12, 1, 2],
            'products': [
                ('Coca Cola 2L', 'Coke'),
                ('Coca Cola 500ml', 'Coke'),
                ('Fanta Orange 2L', 'Fanta'),
                ('Sprite 500ml', 'Sprite'),
                ('Oros 2L', 'Orange'),
                ('Juice 1L', 'Ceres Apple'),
                ('Water 500ml', 'Bonaqua'),
                ('Water 5L', 'Aquartz'),
                ('Milk 1L', 'Clover Fresh'),
            ]
        },
        'Snacks': {
            'price_range': (3, 25),
            'holding_cost_pct': 0.01,
            'seasonality': [3, 4, 6, 7, 12],
            'products': [
                ('Chips 125g', 'Simba Chutney'),
                ('Chips 125g', 'Lays Salt'),
                ('Chips 36g', 'Nik Naks'),
                ('Biscuits', 'Marie'),
                ('Biscuits', 'Tennis'),
                ('Chocolate', 'Cadbury'),
                ('Sweets', 'Jelly Babies'),
                ('Popcorn', 'Act II'),
            ]
        },
        'Personal Care': {
            'price_range': (12, 85),
            'holding_cost_pct': 0.012,
            'seasonality': [1, 2, 9],
            'products': [
                ('Soap', 'Sunlight Bar'),
                ('Soap', 'Lux'),
                ('Toothpaste 100ml', 'Colgate'),
                ('Lotion 400ml', 'Vaseline'),
                ('Deodorant', 'Shield'),
                ('Shampoo 400ml', 'Sunsilk'),
                ('Sanitary Pads', 'Always'),
            ]
        },
        'Household': {
            'price_range': (8, 65),
            'holding_cost_pct': 0.008,
            'seasonality': [1, 4, 12],
            'products': [
                ('Candles 6 pack', 'White'),
                ('Matches Box', 'Lion'),
                ('Washing Powder 1kg', 'Omo'),
                ('Dish Soap 750ml', 'Sunlight'),
                ('Bleach 750ml', 'Jik'),
                ('Toilet Paper 2pk', 'Twinsaver'),
                ('Batteries AA 4pk', 'Eveready'),
            ]
        },
        'Airtime': {
            'price_range': (5, 100),
            'holding_cost_pct': 0.005,
            'seasonality': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'products': [
                ('Airtime P5', 'Mascom'),
                ('Airtime P10', 'Mascom'),
                ('Airtime P25', 'Mascom'),
                ('Airtime P50', 'Orange'),
                ('Data Bundle P20', 'Mascom'),
            ]
        },
        'Bread & Bakery': {
            'price_range': (8, 35),
            'holding_cost_pct': 0.04,
            'seasonality': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'products': [
                ('Bread White', 'Albany'),
                ('Bread Brown', 'Albany'),
                ('Rolls 6 pack', 'Hot Dog'),
            ]
        },
    }
    
    movement_types = ['fast', 'medium', 'slow', 'dead']
    movement_weights = [0.30, 0.35, 0.20, 0.15]
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    products = []
    sku_counter = 1
    
    for category, cat_info in categories.items():
        for product_name, variant in cat_info['products']:
            sku = f"SPZ-{category[:3].upper()}-{str(sku_counter).zfill(4)}"
            sku_counter += 1
            
            full_name = f"{product_name} ({variant})"
            
            unit_cost = round(random.uniform(*cat_info['price_range']), 2)
            markup = random.uniform(1.15, 1.45)
            unit_price = round(unit_cost * markup, 2)
            
            if category in ['Airtime', 'Bread & Bakery']:
                movement = random.choices(['fast', 'medium'], [0.7, 0.3])[0]
            else:
                movement = random.choices(movement_types, movement_weights)[0]
            
            if movement == 'dead':
                stock_date = start_date + timedelta(days=random.randint(0, 180))
            else:
                stock_date = start_date + timedelta(days=random.randint(0, 300))
            
            if movement == 'fast':
                initial_qty = random.randint(30, 100)
            elif movement == 'medium':
                initial_qty = random.randint(20, 60)
            elif movement == 'slow':
                initial_qty = random.randint(10, 40)
            else:
                initial_qty = random.randint(10, 50)
            
            remaining_qty = initial_qty
            current_date = stock_date
            last_sale_date = stock_date
            
            while current_date < end_date and remaining_qty > 0:
                if movement == 'fast':
                    days_gap = random.randint(1, 4)
                    sale_qty = random.randint(3, 15)
                elif movement == 'medium':
                    days_gap = random.randint(3, 14)
                    sale_qty = random.randint(2, 8)
                elif movement == 'slow':
                    days_gap = random.randint(10, 35)
                    sale_qty = random.randint(1, 4)
                else:
                    if random.random() < 0.15:
                        days_gap = random.randint(45, 100)
                        sale_qty = random.randint(1, 2)
                    else:
                        break
                
                current_date += timedelta(days=days_gap)
                
                if current_date.month in cat_info['seasonality']:
                    sale_qty = int(sale_qty * random.uniform(1.3, 2.0))
                
                sale_qty = min(sale_qty, remaining_qty)
                
                if current_date < end_date and sale_qty > 0:
                    last_sale_date = current_date
                    remaining_qty -= sale_qty
            
            total_sold = initial_qty - remaining_qty
            days_since_last_sale = (end_date - last_sale_date).days
            days_in_stock = (end_date - stock_date).days
            
            months_held = days_in_stock / 30
            holding_cost = round(remaining_qty * unit_cost * cat_info['holding_cost_pct'] * months_held, 2)
            
            stock_value = round(remaining_qty * unit_cost, 2)
            velocity = round((total_sold / max(days_in_stock, 1)) * 30, 2)
            
            products.append({
                'sku': sku,
                'product_name': full_name,
                'category': category,
                'unit_cost': unit_cost,
                'unit_price': unit_price,
                'initial_quantity': initial_qty,
                'current_stock': remaining_qty,
                'total_sold': total_sold,
                'stock_received_date': stock_date.strftime('%Y-%m-%d'),
                'last_sale_date': last_sale_date.strftime('%Y-%m-%d'),
                'days_since_last_sale': days_since_last_sale,
                'days_in_stock': days_in_stock,
                'monthly_velocity': velocity,
                'stock_value': stock_value,
                'holding_cost': holding_cost,
                'movement_category': movement
            })
    
    df = pd.DataFrame(products)
    
    df['stock_status'] = df['days_since_last_sale'].apply(
        lambda x: 'Dead Stock (6+ months)' if x > 180 else
                  'Slow Moving (3-6 months)' if x > 90 else
                  'Moderate (1-3 months)' if x > 30 else
                  'Active (< 1 month)'
    )
    
    df['urgency_score'] = df.apply(lambda row: min(
        (row['days_since_last_sale'] / 5) +
        (30 if row['stock_value'] > 500 else 20 if row['stock_value'] > 200 else 10 if row['stock_value'] > 50 else 0) +
        (30 if row['holding_cost'] > 50 else 20 if row['holding_cost'] > 20 else 10 if row['holding_cost'] > 10 else 0),
        100
    ), axis=1)
    
    df['action_required'] = df['stock_status'].apply(
        lambda x: 'Clearance Sale' if x == 'Dead Stock (6+ months)' else
                  'Discount / Promote' if x == 'Slow Moving (3-6 months)' else
                  'Monitor' if x == 'Moderate (1-3 months)' else 'Restock'
    )
    
    return df


# ============== DASH APP ==============

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}]
)

# IMPORTANT: Expose server for Vercel
server = app.server

# Colors
COLORS = {
    'dead': '#dc3545', 'slow': '#fd7e14', 'moderate': '#0dcaf0', 'active': '#198754',
    'primary': '#0d6efd', 'secondary': '#6c757d', 'white': '#ffffff',
    'bg_primary': '#0f172a', 'bg_secondary': '#1e293b', 'bg_page': '#f1f5f9',
    'accent': '#3b82f6', 'success': '#10b981', 'warning': '#f59e0b', 'danger': '#ef4444',
    'text_primary': '#1e293b', 'text_secondary': '#64748b', 'text_muted': '#94a3b8',
    'text_white': '#ffffff', 'border': '#e2e8f0', 'border_light': '#f1f5f9'
}

STATUS_COLORS = {
    'Dead Stock (6+ months)': COLORS['dead'],
    'Slow Moving (3-6 months)': COLORS['slow'],
    'Moderate (1-3 months)': COLORS['moderate'],
    'Active (< 1 month)': COLORS['active']
}

CARD_STYLE = {
    'background': COLORS['white'],
    'borderRadius': '16px',
    'boxShadow': '0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.05)',
    'border': f'1px solid {COLORS["border_light"]}',
    'overflow': 'hidden'
}

SECTION_HEADER_STYLE = {
    'fontSize': '18px', 'fontWeight': '600', 'color': COLORS['text_primary'],
    'marginBottom': '20px', 'display': 'flex', 'alignItems': 'center', 'gap': '10px'
}


# ============== LAYOUT ==============

app.layout = html.Div([
    # Nav
    html.Nav([
        html.Div([
            html.Div([
                html.Div([html.Span("📦", style={'fontSize': '24px'})], style={
                    'width': '44px', 'height': '44px',
                    'background': 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
                    'borderRadius': '12px', 'display': 'flex',
                    'alignItems': 'center', 'justifyContent': 'center'
                }),
                html.Div([
                    html.H1("StockAudit", style={'margin': '0', 'fontSize': '20px', 'fontWeight': '700', 'color': COLORS['text_white']}),
                    html.Span("Spaza Shop Edition", style={'fontSize': '11px', 'color': COLORS['text_muted'], 'textTransform': 'uppercase'})
                ])
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '12px'}),
            html.Div([html.Span("🇧🇼", style={'fontSize': '20px'}), html.Span("BWP", style={'fontSize': '12px', 'fontWeight': '600', 'color': COLORS['text_muted'], 'marginLeft': '6px'})], style={'display': 'flex', 'alignItems': 'center'})
        ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 24px', 'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'height': '70px'})
    ], style={'background': COLORS['bg_primary'], 'borderBottom': f'1px solid {COLORS["bg_secondary"]}'}),
    
    # Upload Section
    html.Div([
        html.Div([
            html.H2("Identify Dead Stock Instantly", style={'fontSize': '28px', 'fontWeight': '700', 'color': COLORS['text_primary'], 'marginBottom': '12px', 'textAlign': 'center'}),
            html.P("Upload your inventory or load demo data to discover trapped cash.", style={'fontSize': '16px', 'color': COLORS['text_secondary'], 'textAlign': 'center', 'marginBottom': '24px'}),
            html.Div([
                dcc.Upload(id='upload-data', children=html.Div(["📁 Upload CSV File"]), style={'padding': '14px 28px', 'background': COLORS['bg_page'], 'border': f'2px dashed {COLORS["border"]}', 'borderRadius': '10px', 'textAlign': 'center', 'cursor': 'pointer', 'fontSize': '14px', 'fontWeight': '500', 'color': COLORS['text_secondary']}, multiple=False),
                html.Span("or", style={'color': COLORS['text_muted'], 'fontSize': '14px', 'margin': '0 16px'}),
                html.Button(["▶ Load Demo Data"], id='load-sample', style={'padding': '14px 28px', 'background': 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)', 'color': 'white', 'border': 'none', 'borderRadius': '10px', 'fontSize': '14px', 'fontWeight': '600', 'cursor': 'pointer'})
            ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'flexWrap': 'wrap', 'gap': '10px'}),
            html.Div(id='upload-status', style={'marginTop': '16px', 'textAlign': 'center'})
        ], style={'maxWidth': '600px', 'margin': '0 auto'})
    ], style={'padding': '48px 24px', 'background': COLORS['white']}),
    
    dcc.Store(id='inventory-data'),
    html.Div(id='dashboard-content', style={'display': 'none'})
], style={'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', 'background': COLORS['bg_page'], 'minHeight': '100vh', 'margin': '0'})


# ============== HELPERS ==============

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        return pd.read_csv(io.StringIO(decoded.decode('utf-8'))), None
    except Exception as e:
        return None, str(e)

def process_data(df):
    required = ['sku', 'product_name', 'category', 'unit_cost', 'current_stock']
    missing = [c for c in required if c not in df.columns]
    if missing:
        return None, f"Missing: {', '.join(missing)}"
    
    if 'stock_value' not in df.columns:
        df['stock_value'] = df['current_stock'] * df['unit_cost']
    if 'days_since_last_sale' not in df.columns:
        df['days_since_last_sale'] = 0
    if 'stock_status' not in df.columns:
        df['stock_status'] = df['days_since_last_sale'].apply(lambda x: 'Dead Stock (6+ months)' if x > 180 else 'Slow Moving (3-6 months)' if x > 90 else 'Moderate (1-3 months)' if x > 30 else 'Active (< 1 month)')
    if 'urgency_score' not in df.columns:
        df['urgency_score'] = 50
    if 'holding_cost' not in df.columns:
        df['holding_cost'] = 0
    if 'action_required' not in df.columns:
        df['action_required'] = 'Review'
    return df, None

def create_metric_card(icon, title, value, subtitle, color=None):
    return html.Div([
        html.Div([html.Span(icon, style={'fontSize': '20px'})], style={'width': '48px', 'height': '48px', 'background': f'{color}15' if color else COLORS['bg_page'], 'borderRadius': '12px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'marginBottom': '12px'}),
        html.P(title, style={'fontSize': '12px', 'color': COLORS['text_muted'], 'margin': '0 0 6px 0', 'fontWeight': '500', 'textTransform': 'uppercase'}),
        html.H3(value, style={'fontSize': '24px', 'fontWeight': '700', 'color': color if color else COLORS['text_primary'], 'margin': '0 0 4px 0'}),
        html.Span(subtitle, style={'fontSize': '12px', 'color': COLORS['text_secondary']})
    ], style={**CARD_STYLE, 'padding': '20px'})

def create_kpi_section(df):
    dead = df[df['stock_status'] == 'Dead Stock (6+ months)']
    slow = df[df['stock_status'] == 'Slow Moving (3-6 months)']
    active = df[df['stock_status'] == 'Active (< 1 month)']
    return html.Div([
        create_metric_card("💀", "Dead Stock", f"P{dead['stock_value'].sum():,.0f}", f"{len(dead)} items", COLORS['danger']),
        create_metric_card("🐌", "Slow Moving", f"P{slow['stock_value'].sum():,.0f}", f"{len(slow)} items", COLORS['warning']),
        create_metric_card("✅", "Active Stock", f"P{active['stock_value'].sum():,.0f}", f"{len(active)} items", COLORS['success']),
        create_metric_card("💰", "Total Value", f"P{df['stock_value'].sum():,.0f}", f"{len(df)} products", COLORS['accent'])
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(180px, 1fr))', 'gap': '16px', 'marginBottom': '24px'})

def create_status_chart(df):
    summary = df.groupby('stock_status')['stock_value'].sum().reset_index()
    fig = go.Figure(data=[go.Pie(labels=summary['stock_status'], values=summary['stock_value'], hole=0.6, marker=dict(colors=[STATUS_COLORS.get(s, COLORS['secondary']) for s in summary['stock_status']]), textinfo='percent', hovertemplate="<b>%{label}</b><br>P%{value:,.0f}<extra></extra>")])
    fig.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5), margin=dict(t=20, b=60, l=20, r=20), height=300, paper_bgcolor='rgba(0,0,0,0)')
    return fig

def create_category_chart(df):
    problem = df[df['stock_status'].isin(['Dead Stock (6+ months)', 'Slow Moving (3-6 months)'])]
    if len(problem) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No problem stock! 🎉", x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)')
        return fig
    cat_summary = problem.groupby('category')['stock_value'].sum().sort_values(ascending=True).reset_index()
    fig = go.Figure(go.Bar(y=cat_summary['category'], x=cat_summary['stock_value'], orientation='h', marker=dict(color=COLORS['danger'])))
    fig.update_layout(xaxis_title="Stock Value (P)", margin=dict(t=20, b=50, l=100, r=20), height=300, paper_bgcolor='rgba(0,0,0,0)')
    return fig

def create_worst_products_chart(df):
    dead = df[df['stock_status'] == 'Dead Stock (6+ months)'].nlargest(8, 'stock_value')
    if len(dead) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No dead stock! 🎉", x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)')
        return fig
    dead = dead.copy()
    dead['short_name'] = dead['product_name'].apply(lambda x: x[:25] + '...' if len(str(x)) > 25 else x)
    fig = go.Figure(go.Bar(x=dead['stock_value'], y=dead['short_name'], orientation='h', marker=dict(color=COLORS['danger']), text=[f"P{v:,.0f}" for v in dead['stock_value']], textposition='outside'))
    fig.update_layout(xaxis_title="Stock Value (P)", margin=dict(t=20, b=50, l=160, r=60), height=320, paper_bgcolor='rgba(0,0,0,0)', yaxis=dict(autorange='reversed'))
    return fig

def create_priority_table(df):
    priority = df.nlargest(8, 'urgency_score')[['product_name', 'category', 'current_stock', 'stock_value', 'days_since_last_sale', 'action_required']].copy()
    return dash_table.DataTable(data=priority.to_dict('records'), columns=[{'name': 'Product', 'id': 'product_name'}, {'name': 'Category', 'id': 'category'}, {'name': 'Stock', 'id': 'current_stock'}, {'name': 'Value (P)', 'id': 'stock_value', 'type': 'numeric', 'format': {'specifier': ',.0f'}}, {'name': 'Days Idle', 'id': 'days_since_last_sale'}, {'name': 'Action', 'id': 'action_required'}], style_table={'overflowX': 'auto'}, style_cell={'textAlign': 'left', 'padding': '12px', 'fontSize': '13px'}, style_header={'backgroundColor': COLORS['bg_page'], 'fontWeight': '600', 'fontSize': '11px', 'textTransform': 'uppercase'}, page_size=8)


# ============== CALLBACK ==============

@app.callback(
    [Output('inventory-data', 'data'), Output('upload-status', 'children'), Output('dashboard-content', 'style'), Output('dashboard-content', 'children')],
    [Input('upload-data', 'contents'), Input('load-sample', 'n_clicks')],
    [State('upload-data', 'filename')]
)
def update_dashboard(contents, n_clicks, filename):
    ctx = callback_context
    if not ctx.triggered:
        return None, "", {'display': 'none'}, None
    
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger == 'load-sample' and n_clicks:
        df = generate_spaza_inventory()  # Now uses embedded function
        status = html.Span("✓ Demo data loaded", style={'color': COLORS['success']})
    elif trigger == 'upload-data' and contents:
        df, error = parse_contents(contents, filename)
        if error:
            return None, html.Span(f"✗ {error}", style={'color': COLORS['danger']}), {'display': 'none'}, None
        df, error = process_data(df)
        if error:
            return None, html.Span(f"✗ {error}", style={'color': COLORS['danger']}), {'display': 'none'}, None
        status = html.Span(f"✓ Loaded {len(df)} products", style={'color': COLORS['success']})
    else:
        return None, "", {'display': 'none'}, None
    
    dashboard = html.Div([
        html.Div([
            create_kpi_section(df),
            html.Div([
                html.Div([html.H3("📈 Stock Distribution", style={'fontSize': '16px', 'marginBottom': '16px'}), dcc.Graph(figure=create_status_chart(df), config={'displayModeBar': False})], style={**CARD_STYLE, 'padding': '20px'}),
                html.Div([html.H3("📦 Problem by Category", style={'fontSize': '16px', 'marginBottom': '16px'}), dcc.Graph(figure=create_category_chart(df), config={'displayModeBar': False})], style={**CARD_STYLE, 'padding': '20px'})
            ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(350px, 1fr))', 'gap': '20px', 'marginBottom': '20px'}),
            html.Div([html.H3("🔥 Top Dead Stock Items", style={'fontSize': '16px', 'marginBottom': '16px'}), dcc.Graph(figure=create_worst_products_chart(df), config={'displayModeBar': False})], style={**CARD_STYLE, 'padding': '20px', 'marginBottom': '20px'}),
            html.Div([html.H3("🎯 Priority Actions", style={'fontSize': '16px', 'marginBottom': '16px'}), create_priority_table(df)], style={**CARD_STYLE, 'padding': '20px', 'marginBottom': '20px'}),
            html.Div([html.Span("📦 StockAudit • Spaza Shop Edition • Made for Botswana 🇧🇼", style={'color': COLORS['text_muted'], 'fontSize': '13px'})], style={'textAlign': 'center', 'padding': '20px'})
        ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '24px'})
    ], style={'background': COLORS['bg_page']})
    
    return df.to_json(), status, {'display': 'block'}, dashboard


# ============== FOR VERCEL ==============
# The 'server' variable is what Vercel needs
# Do NOT call app.run_server() on Vercel

if __name__ == '__main__':
    # Only runs locally, not on Vercel
    app.run_server(debug=True, port=8050)