"""
Use:
    python Interpreter.py {.bumbuojam script path} {cleaned .csv file path}

Returns:
    {plot .html file path} {plot .png file path}
"""

import sys
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

def parse_bumbuojam_file(file_path):
    """Parse a .bumbuojam file and extract plot configuration."""
    with open(file_path, 'r') as file:
        content = file.read()
        
    # Extract key-value pairs
    config = {}
    for line in content.strip().split('\n'):
        if ':' in line and not line.strip().startswith('//'):
            key, value = line.split(':', 1)
            config[key.strip()] = value.strip()
        
    return config

# Returns flag 1 if a dataframe was returned, 0 if a series was returned, and -1 if a string was returned
def apply_function(X, func_str, df):
    """Apply a function defined in the .bumbuojam language to the dataframe."""
    # Check if it's a direct column reference
    if func_str in df.columns:
        return [0, df[func_str]]
        
    # Parse function calls
    if 'SUM(' in func_str:
        match = re.search(r'SUM\((.*?)\)', func_str)
        if match:
            x_col, y_col = X, match.group(1).strip()
            return [1, df.groupby(x_col, sort=False)[y_col].sum()]
        
    elif 'MEAN(' in func_str:
        match = re.search(r'MEAN\((.*?)\)', func_str)
        if match:
            x_col, y_col = X, match.group(1).strip()
            return [1, df.groupby(x_col, sort=False)[y_col].mean()]
        
    elif 'COUNT()' in func_str:
        return [1, df[X].value_counts()]

    elif 'PERCENTAGE(' in func_str:
        match = re.search(r'PERCENTAGE\((.*?)\)', func_str)
        if match:
            x_col, y_col = X, match.group(1).strip()
            grouped = df.groupby(x_col, sort=False)[y_col].sum()
            return [1, (grouped / grouped.sum()) * 100]

    # If no function match or direct column, return the string itself
    return [-1, func_str]

def reshape(data, var, x):
    new_data = []
    for i in range(len(x)):
        return
        #new_data.append(df.loc[df[config.get('X', '')] == X[i], config.get('Z', '')].values[0])

def get_vars(config, df):
    # Apply functions for X, Y, and Z if defined       
        var_str = [
            config.get('X', ''),
            config.get('Y', ''),
            config.get('Z', ''),
            config.get('COLOR', ''),
            config.get('SIZE', '')
            ]

        raw_data = []

        for str in var_str:
            raw_data.append(apply_function(var_str[0], str, df))

        num_aggr = 0
        num_nagg = 0
        for i in range(1, len(raw_data)):
            data = raw_data[i]
            if data[0] == 1:
                num_aggr += 1
            elif data[0] == 0:
                num_nagg += 1


        if num_aggr > 0:
            if num_nagg > 0:
                print("ERROR: Cannot mix aggregated and non-aggregated data")
                sys.exit(1)
            raw_data[0] = [0, raw_data[1][1].index.to_series()]

            
        # maybe add dimension match check


        return raw_data

def get_options(config):
    TYPE = config.get('TYPE', 'SCATTERPLOT')
    X_name = config.get('X_name', '')
    Y_name = config.get('Y_name', '')
    Z_name = config.get('Z_name', '')
    COLOR = config.get('COLOR', '')
    SIZE = config.get('SIZE', '')
    SCALE = config.get('SCALE', '')
    TRENDLINE = config.get('TRENDLINE', '')
    NORMALIZE = config.get('NORMALIZE', '')
    NBINS = config.get('NBINS', '')
    POINTS = config.get('POINTS', '')
    BOXLINE = config.get('BOXLINE', '')
    BARMODE = config.get('BARMODE', '')
    
    return [TYPE, COLOR, SIZE, SCALE, TRENDLINE, NORMALIZE, NBINS, POINTS, BOXLINE, BARMODE, X_name, Y_name, Z_name]

def reshape_var(vars):
    new_vars = []

    for i in range(len(vars)):
        new_vars.append(vars[i][1])

    return new_vars

def generate_plot(vars, opts, config):
    """
    Generate a plot based on the specified type and options from .bumbuojam file.
    
    Args:
        vars: List of variables [X, Y, Z, COLOR, SIZE]
        opts: List of options [TYPE, COLOR, SIZE, SCALE, TRENDLINE, NORMALIZE, NBINS, POINTS, BOXLINE, BARMODE]
        config: Original configuration dictionary
    
    Returns:
        Plotly figure object
    """
    # Unpack variables
    X, Y = vars[0], vars[1]
    if(isinstance(vars[2], pd.Series)):
        Z = vars[2]
    else:
        Z= None
    if(isinstance(vars[3], pd.Series)):
        COLOR = vars[3]
    else:
        COLOR = None
    if(isinstance(vars[4], pd.Series)):
        SIZE = vars[4]
    else:
        SIZE = None
    
    # Unpack options
    TYPE = opts[0]
    SCALE = opts[3] if len(opts) > 3 and opts[3] != 'null' else None
    TRENDLINE = True if len(opts) > 4 and opts[4] == 'true' else None
    NORMALIZE = True if len(opts) > 5 and opts[5] == 'true' else None
    NBINS = int(opts[6]) if len(opts) > 6 and opts[6] and opts[6] != 'null' else None
    POINTS = opts[7] if len(opts) > 7 and opts[7] and opts[7] != 'null' else None
    BOXLINE = opts[8] if len(opts) > 8 and opts[8] and opts[8] != 'null' else None
    BARMODE = opts[9] if len(opts) > 9 and opts[9] and opts[9] != 'null' else 'group'
    X_name = opts[10] if len(opts) > 10 and opts[10] != 'null' else None
    Y_name = opts[11] if len(opts) > 11 and opts[11] != 'null' else None
    Z_name = opts[12] if len(opts) > 12 and opts[12] != 'null' else None
    
    title = config.get('TITLE', 'Plot Title').strip('"')  # Remove quotes if present
    
    # Create a dataframe from the arrays for consistent handling
    data = {'x': X}
    data['y'] = Y
    if Z is not None:
        data['z'] = Z
    if COLOR is not None:
        data['color'] = COLOR
    if SIZE is not None:
        data['size'] = SIZE
    
    df = pd.DataFrame(data)
    # Create the figure based on plot type
    if TYPE == "SCATTERPLOT":
        if Z is not None:
            fig = px.scatter_3d(df, x='x', y='y', z='z', 
                                color=COLOR,
                                size=SIZE,
                                title=title,
                                labels={X: X_name, Y: Y_name, Z: Z_name})
        else:
            fig = px.scatter(df, x='x', y='y',
                             color='color',
                             size=SIZE,
                             trendline='ols' if TRENDLINE else None,
                             title=title,
                             labels={'x': X_name, 'y': Y_name})
    
    elif TYPE == "HISTOGRAM":
        fig = px.histogram(df, x='x', y='y' if Y is not None else None,
                           color=COLOR,
                           nbins=NBINS,
                           histnorm='probability' if NORMALIZE else None,
                           title=title,
                           labels={'x': X_name, 'y': Y_name})
    
    elif TYPE == "LINEPLOT":
        fig = px.line(df, x='x', y='y',
                      title=title,
                      labels={'x': X_name, 'y': Y_name})
    
    elif TYPE == "BARCHART":
        fig = px.bar(df, x='x', y='y',
                     color=COLOR,
                     barmode=BARMODE,
                     title=title,
                     labels={'x': X_name, 'y': Y_name})
    
    elif TYPE == "HEATMAP":
        if Z is not None:
            # Pivot the data for the heatmap
            pivot_df = df.pivot(index='y', columns='x', values='z')
            fig = px.imshow(pivot_df, color_continuous_scale=SCALE or 'viridis', title=title,
            labels={'x': X_name, 'y': Y_name, 'z': Z_name})
        else:
            # For 2D heatmap (count of occurrences)
            pivot_df = pd.crosstab(df['y'], df['x'])
            fig = px.imshow(pivot_df, color_continuous_scale=SCALE or 'viridis', title=title, 
                            labels={'x': X_name, 'y': Y_name})
    
    elif TYPE == "PIECHART":
        fig = px.pie(df, values='y', names='x',
                     title=title,
                     labels={'x': X_name, 'y': Y_name})
        
    elif TYPE == "VIOLINPLOT":
        fig = px.violin(df, x='x', y='y',
                        color=COLOR,
                        box=True,
                        points=POINTS or False,
                        title=title,
                        labels={'x': X_name, 'y': Y_name})
    
    elif TYPE == "BOXPLOT":
        fig = px.box(df, x='x', y='y',
                     color=COLOR,
                     title=title,
                     labels={'x': X_name, 'y': Y_name})
        if BOXLINE:
            line_style = {'solid': 'solid', 'dashed': 'dash', 'dotted': 'dot'}.get(BOXLINE, 'solid')
            fig.update_traces(line=dict(dash=line_style))
    
    else:
        # Default to scatter if type not recognized
        print(f"Warning: Plot type '{TYPE}' not recognized. Defaulting to SCATTERPLOT.")
        fig = px.scatter(df, x='x', y='y', title=title)
    
    # Apply additional styling as needed
    fig.update_layout(
        title=title,
        plot_bgcolor='white',
        legend_title_text='Legend'
    )
    
    return fig

def main():
    if len(sys.argv) != 3:
        print("Usage: python Interpreter.py {.bumbuojam path} {.csv path}")
        sys.exit(1)

    bum_path = sys.argv[1]
    csv_path = sys.argv[2]
    
    name = bum_path.split('.')[-2].split('/')[-1]
    print(name)

    cwd = os.getcwd()

    plot_image_path = cwd + f'/Ai/VizualizationFiles/{name}.png'
    plot_html_path = cwd + f'/Ai/VizualizationFiles/{name}.html'

    if not bum_path.endswith('.bumbuojam'):
        print("Error: File must have .bumbuojam extension. Tu ka, nebuombuoji?")
        sys.exit(1)
    
    if not os.path.exists(bum_path):
        print(f"Error: File {bum_path} does not exist")
        sys.exit(1)
    
    try:
        # Load data
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        else:
            print(f"Warning: No data file found at {csv_path}")
            return
            
        # Parse the configuration
        config = parse_bumbuojam_file(bum_path)
        
        # Get all the goodies
        vars = get_vars(config, df)
        vars = reshape_var(vars)
        opts = get_options(config)

        # Generate and pray
        fig = generate_plot(vars, opts, config)
        fig.write_image(plot_image_path)
        fig.write_html(plot_html_path)

        print(f"{plot_html_path}\n{plot_image_path}")
        return plot_html_path, plot_image_path
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
