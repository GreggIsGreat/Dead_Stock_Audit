import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_spaza_inventory(num_products=120, seed=42):
    """
    Generate realistic Spaza Shop inventory data for Botswana
    - Prices in BWP (Botswana Pula)
    - Products typical of spaza shops
    - Seasonal patterns (holidays, school terms, weather)
    - Correlations between product types and movement
    """
    
    np.random.seed(seed)
    random.seed(seed)
    
    # Spaza shop categories with BWP price ranges and characteristics
    categories = {
        'Groceries': {
            'price_range': (8, 120),
            'holding_cost_pct': 0.02,
            'seasonality': [12, 1, 4],  # Holidays, back to school
            'products': [
                ('Maize Meal 2.5kg', 'White Star'),
                ('Maize Meal 5kg', 'White Star'),
                ('Maize Meal 1kg', 'Iwisa'),
                ('Cooking Oil 750ml', 'Sunfoil'),
                ('Cooking Oil 2L', 'Golden Fry'),
                ('Sugar 2kg', 'White'),
                ('Sugar 1kg', 'Brown'),
                ('Rice 2kg', 'Tastic'),
                ('Rice 1kg', 'Spekko'),
                ('Flour 2.5kg', 'Snowflake'),
                ('Salt 500g', 'Cerebos'),
                ('Tea 100 bags', 'Five Roses'),
                ('Tea 50 bags', 'Joko'),
                ('Coffee 200g', 'Ricoffy'),
                ('Beans 410g', 'KOO'),
                ('Pilchards 400g', 'Lucky Star'),
                ('Chakalaka 410g', 'KOO'),
                ('Tomato Sauce 700ml', 'All Gold'),
                ('Peanut Butter 400g', 'Black Cat'),
                ('Jam 450g', 'Fynbos'),
                ('Milk Powder 400g', 'Nespray'),
                ('Custard 500g', 'Ultramel'),
            ]
        },
        'Beverages': {
            'price_range': (5, 35),
            'holding_cost_pct': 0.015,
            'seasonality': [10, 11, 12, 1, 2],  # Hot season
            'products': [
                ('Coca Cola 2L', 'Coke'),
                ('Coca Cola 500ml', 'Coke'),
                ('Fanta Orange 2L', 'Fanta'),
                ('Sprite 500ml', 'Sprite'),
                ('Oros 2L', 'Orange'),
                ('Oros 2L', 'Tropical'),
                ('Mazoe 2L', 'Orange'),
                ('Juice 1L', 'Ceres Apple'),
                ('Juice 1L', 'Liqui Fruit'),
                ('Water 500ml', 'Bonaqua'),
                ('Water 5L', 'Aquartz'),
                ('Energy Drink', 'Score'),
                ('Energy Drink', 'Red Bull'),
                ('Milk 1L', 'Clover Fresh'),
                ('Milk 1L', 'Steri Stumpie'),
                ('Yoghurt 1kg', 'Danone'),
            ]
        },
        'Snacks': {
            'price_range': (3, 25),
            'holding_cost_pct': 0.01,
            'seasonality': [3, 4, 6, 7, 12],  # School holidays
            'products': [
                ('Chips 125g', 'Simba Chutney'),
                ('Chips 125g', 'Lays Salt'),
                ('Chips 36g', 'Nik Naks'),
                ('Chips 125g', 'Doritos'),
                ('Biscuits', 'Marie'),
                ('Biscuits', 'Tennis'),
                ('Biscuits', 'Romany Creams'),
                ('Biscuits', 'Oreos'),
                ('Chocolate', 'Cadbury Dairy Milk'),
                ('Chocolate', 'Bar One'),
                ('Chocolate', 'KitKat'),
                ('Sweets', 'Jelly Babies'),
                ('Sweets', 'Wine Gums'),
                ('Sweets', 'Chappies'),
                ('Popcorn', 'Act II'),
                ('Nuts 100g', 'Peanuts Salted'),
                ('Dried Fruit', 'Safari Mix'),
            ]
        },
        'Personal Care': {
            'price_range': (12, 85),
            'holding_cost_pct': 0.012,
            'seasonality': [1, 2, 9],  # New year, back to school
            'products': [
                ('Soap', 'Sunlight Bar'),
                ('Soap', 'Lux'),
                ('Soap', 'Dettol'),
                ('Toothpaste 100ml', 'Colgate'),
                ('Toothpaste 50ml', 'Aquafresh'),
                ('Lotion 400ml', 'Vaseline'),
                ('Lotion 200ml', 'Dawn'),
                ('Petroleum Jelly 250ml', 'Vaseline'),
                ('Deodorant', 'Shield'),
                ('Deodorant', 'Axe'),
                ('Shampoo 400ml', 'Sunsilk'),
                ('Body Wash 400ml', 'Dettol'),
                ('Roll-on', 'Nivea'),
                ('Face Cream', 'Pond\'s'),
                ('Hair Food', 'Sta Sof Fro'),
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
                ('Washing Powder 2kg', 'Sunlight'),
                ('Dish Soap 750ml', 'Sunlight'),
                ('Bleach 750ml', 'Jik'),
                ('Floor Polish 750ml', 'Cobra'),
                ('Air Freshener', 'Airoma'),
                ('Toilet Paper 2pk', 'Twinsaver'),
                ('Paper Towels', 'Checkers'),
                ('Refuse Bags 20s', 'Black'),
                ('Sponge Scourers', 'Scrub'),
                ('Steel Wool', 'Brillo'),
                ('Insect Spray', 'Doom'),
                ('Batteries AA 4pk', 'Eveready'),
            ]
        },
        'Airtime & Essentials': {
            'price_range': (5, 100),
            'holding_cost_pct': 0.005,
            'seasonality': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],  # Always needed
            'products': [
                ('Airtime P5', 'Mascom'),
                ('Airtime P10', 'Mascom'),
                ('Airtime P25', 'Mascom'),
                ('Airtime P50', 'Mascom'),
                ('Airtime P5', 'Orange'),
                ('Airtime P10', 'Orange'),
                ('Airtime P25', 'Orange'),
                ('Airtime P10', 'BTC'),
                ('Data Bundle P20', 'Mascom'),
                ('Data Bundle P50', 'Mascom'),
                ('Electricity Voucher', 'BPC'),
                ('Prepaid Water', 'WUC'),
            ]
        },
        'Bread & Bakery': {
            'price_range': (8, 35),
            'holding_cost_pct': 0.04,  # Higher due to perishability
            'seasonality': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],  # Daily staple
            'products': [
                ('Bread White', 'Albany'),
                ('Bread Brown', 'Albany'),
                ('Bread White', 'Blue Ribbon'),
                ('Bread Whole Wheat', 'Sasko'),
                ('Rolls 6 pack', 'Hot Dog'),
                ('Scones 6 pack', 'Fresh'),
                ('Vetkoek 4 pack', 'Fresh'),
                ('Fat Cakes 6 pack', 'Homemade'),
            ]
        },
        'Tobacco & Extras': {
            'price_range': (25, 80),
            'holding_cost_pct': 0.008,
            'seasonality': [12, 1, 6],
            'products': [
                ('Cigarettes', 'Peter Stuyvesant'),
                ('Cigarettes', 'Dunhill'),
                ('Cigarettes', 'Rothmans'),
                ('Cigarettes', 'Pacific'),
                ('Loose Tobacco', 'Boxer'),
                ('Rolling Paper', 'Rizla'),
                ('Lighters 3pk', 'Bic'),
            ]
        }
    }
    
    # Movement patterns
    movement_types = ['fast', 'medium', 'slow', 'dead']
    movement_weights = [0.30, 0.35, 0.20, 0.15]
    
    # Generate dates (1 year ending today)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    products = []
    sku_counter = 1
    
    for category, cat_info in categories.items():
        for product_name, variant in cat_info['products']:
            # Generate SKU
            sku = f"SPZ-{category[:3].upper()}-{str(sku_counter).zfill(4)}"
            sku_counter += 1
            
            full_name = f"{product_name} ({variant})"
            
            # Price in Pula
            unit_cost = round(random.uniform(*cat_info['price_range']), 2)
            markup = random.uniform(1.15, 1.45)  # 15-45% markup typical for spaza
            unit_price = round(unit_cost * markup, 2)
            
            # Determine movement pattern
            # Airtime and bread are typically fast movers
            if category in ['Airtime & Essentials', 'Bread & Bakery']:
                movement = random.choices(['fast', 'medium'], [0.7, 0.3])[0]
            elif category == 'Tobacco & Extras':
                movement = random.choices(['fast', 'medium', 'slow'], [0.4, 0.4, 0.2])[0]
            else:
                movement = random.choices(movement_types, movement_weights)[0]
            
            # Stock received date
            if movement == 'dead':
                stock_date = start_date + timedelta(days=random.randint(0, 180))
            else:
                stock_date = start_date + timedelta(days=random.randint(0, 300))
            
            # Initial quantity based on movement and category
            if movement == 'fast':
                if category in ['Airtime & Essentials']:
                    initial_qty = random.randint(50, 200)
                else:
                    initial_qty = random.randint(30, 100)
            elif movement == 'medium':
                initial_qty = random.randint(20, 60)
            elif movement == 'slow':
                initial_qty = random.randint(10, 40)
            else:  # dead
                initial_qty = random.randint(10, 50)
            
            # Simulate sales
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
                else:  # dead
                    if random.random() < 0.15:
                        days_gap = random.randint(45, 100)
                        sale_qty = random.randint(1, 2)
                    else:
                        break
                
                current_date += timedelta(days=days_gap)
                
                # Seasonality boost
                if current_date.month in cat_info['seasonality']:
                    sale_qty = int(sale_qty * random.uniform(1.3, 2.0))
                
                sale_qty = min(sale_qty, remaining_qty)
                
                if current_date < end_date and sale_qty > 0:
                    last_sale_date = current_date
                    remaining_qty -= sale_qty
            
            # Calculate metrics
            total_sold = initial_qty - remaining_qty
            days_since_last_sale = (end_date - last_sale_date).days
            days_in_stock = (end_date - stock_date).days
            
            # Holding cost (monthly rate)
            months_held = days_in_stock / 30
            holding_cost = round(remaining_qty * unit_cost * cat_info['holding_cost_pct'] * months_held, 2)
            
            # Values
            stock_value = round(remaining_qty * unit_cost, 2)
            potential_revenue = round(remaining_qty * unit_price, 2)
            
            # Velocity
            velocity = round((total_sold / max(days_in_stock, 1)) * 30, 2)
            
            # Profit margin
            profit_margin = round(((unit_price - unit_cost) / unit_price) * 100, 1)
            
            products.append({
                'sku': sku,
                'product_name': full_name,
                'category': category,
                'unit_cost': unit_cost,
                'unit_price': unit_price,
                'profit_margin_pct': profit_margin,
                'initial_quantity': initial_qty,
                'current_stock': remaining_qty,
                'total_sold': total_sold,
                'stock_received_date': stock_date.strftime('%Y-%m-%d'),
                'last_sale_date': last_sale_date.strftime('%Y-%m-%d'),
                'days_since_last_sale': days_since_last_sale,
                'days_in_stock': days_in_stock,
                'monthly_velocity': velocity,
                'stock_value': stock_value,
                'potential_revenue': potential_revenue,
                'holding_cost': holding_cost,
                'movement_category': movement
            })
    
    df = pd.DataFrame(products)
    
    # Add classifications
    df['stock_status'] = df['days_since_last_sale'].apply(classify_stock)
    df['urgency_score'] = df.apply(calculate_urgency, axis=1)
    df['action_required'] = df.apply(suggest_action, axis=1)
    
    return df


def classify_stock(days):
    """Classify stock based on days since last sale"""
    if days > 180:
        return 'Dead Stock (6+ months)'
    elif days > 90:
        return 'Slow Moving (3-6 months)'
    elif days > 30:
        return 'Moderate (1-3 months)'
    else:
        return 'Active (< 1 month)'


def calculate_urgency(row):
    """Calculate urgency score 0-100"""
    score = 0
    
    # Days since last sale (max 40 points)
    score += min(row['days_since_last_sale'] / 5, 40)
    
    # Stock value tied up (max 30 points) - adjusted for Pula
    if row['stock_value'] > 500:
        score += 30
    elif row['stock_value'] > 200:
        score += 20
    elif row['stock_value'] > 50:
        score += 10
    
    # Holding cost (max 30 points)
    if row['holding_cost'] > 50:
        score += 30
    elif row['holding_cost'] > 20:
        score += 20
    elif row['holding_cost'] > 10:
        score += 10
    
    return min(round(score, 1), 100)


def suggest_action(row):
    """Suggest action based on stock status"""
    if row['stock_status'] == 'Dead Stock (6+ months)':
        return 'Clearance Sale / Bundle'
    elif row['stock_status'] == 'Slow Moving (3-6 months)':
        return 'Discount / Promote'
    elif row['stock_status'] == 'Moderate (1-3 months)':
        return 'Monitor Weekly'
    else:
        return 'Restock When Low'


if __name__ == "__main__":
    import os
    os.makedirs('sample_data', exist_ok=True)
    
    df = generate_spaza_inventory(num_products=120)
    df.to_csv('sample_data/inventory_records.csv', index=False)
    
    print(f"✅ Generated {len(df)} products for Spaza Shop")
    print(f"\n📊 Stock Status Distribution:")
    print(df['stock_status'].value_counts())
    print(f"\n💰 Total Dead Stock Value: P{df[df['stock_status'] == 'Dead Stock (6+ months)']['stock_value'].sum():,.2f}")
    print(f"📦 Categories: {df['category'].nunique()}")