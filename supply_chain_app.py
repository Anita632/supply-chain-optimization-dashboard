import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from io import StringIO
from scipy.spatial import distance_matrix
import numpy as np
from PIL import Image

# MUST BE THE FIRST Streamlit COMMAND
st.set_page_config(page_title="Supply Chain Optimization Dashboard", layout="wide")


@st.cache_data
def load_data():
    # URL to the CSV file in your GitHub repository
    url = 'https://raw.githubusercontent.com/Anita632/supply-chain-optimization-dashboard/refs/heads/main/cleaned_supply_chain_data.csv'
    return pd.read_csv(url)

data = load_data()
st.write(data.head())



st.title("Supply Chain Optimization Dashboard")

# Upload CSV file
uploaded_file = st.file_uploader("C:/Users/yadav/OneDrive/Desktop/Anita/cleaned_supply_chain_data.csv", type="csv")


if uploaded_file is not None:
    # Read the CSV file
    try:
        df = pd.read_csv(uploaded_file)
        st.write("File Uploaded Successfully!")
        
        # Check for required columns
        if all(col in df.columns for col in ['Source', 'Destination', 'Cost']):
            
            # Create a directed graph
            G = nx.DiGraph()
            
            # Add edges to the graph
            for index, row in df.iterrows():
                G.add_edge(row['Source'], row['Destination'], weight=row['Cost'])
            
            st.subheader("Route Optimization: Shortest Path")
            
            # Extract unique sources and destinations from the dataset
            unique_sources = df['Source'].unique().tolist()
            unique_destinations = df['Destination'].unique().tolist()
            
            # Show dropdowns with filtered lists
            source_node = st.selectbox("Select the Source Node", unique_sources)
            destination_node = st.selectbox("Select the Destination Node", unique_destinations)
            
            if st.button("Find Shortest Path"):
                try:
                    # Calculate shortest path
                    shortest_path = nx.shortest_path(G, source=source_node, target=destination_node, weight='weight')
                    shortest_distance = nx.shortest_path_length(G, source=source_node, target=destination_node, weight='weight')
                    
                    # Display results
                    st.success(f"Shortest Path from {source_node} to {destination_node}: {' -> '.join(shortest_path)}")
                    st.success(f"Total Distance: {shortest_distance}")
                    
                    # Plotting the shortest path
                    pos = nx.spring_layout(G, seed=42)
                    plt.figure(figsize=(10, 6))
                    
                    # Draw the complete graph in light grey
                    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightgrey', font_size=12, font_color='black')
                    
                    # Highlight the shortest path in red
                    path_edges = list(zip(shortest_path, shortest_path[1:]))
                    nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color='red')
                    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
                    
                    plt.title("Shortest Path Visualization")
                    st.pyplot(plt)
                    
                except nx.NetworkXNoPath:
                    st.error("No path exists between the specified nodes.")
                except Exception as e:
                    st.error(f"Error: {e}")
            
            # Minimum Spanning Tree Section
            st.subheader("Minimum Spanning Tree")
            
            if st.button("Find Minimum Spanning Tree"):
                try:
                    # Convert directed graph to undirected for MST calculation
                    undirected_G = G.to_undirected()
                    mst = nx.minimum_spanning_tree(undirected_G, weight='weight')
                    
                    # Plot the MST
                    plt.figure(figsize=(10, 6))
                    pos = nx.spring_layout(mst, seed=42)
                    edge_labels = nx.get_edge_attributes(mst, 'weight')
                    
                    nx.draw(mst, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=12, font_color='black')
                    nx.draw_networkx_edge_labels(mst, pos, edge_labels=edge_labels)
                    
                    plt.title("Minimum Spanning Tree Visualization")
                    st.pyplot(plt)
                    
                    st.success("Minimum Spanning Tree generated successfully!")
                    
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("Column names are incorrect! Make sure your CSV file has columns 'Source', 'Destination', 'Cost'.")
    except Exception as e:
        st.error(f"Error reading file: {e}")
