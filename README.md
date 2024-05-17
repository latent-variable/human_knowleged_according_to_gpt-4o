
# Human Knowledge Timeline Visualization

## Overview

This project aims to visualize the evolution of human knowledge over time, utilizing a dynamic and interactive 2D graph. The graph plots significant milestones in human knowledge, categorized by different fields such as Technology, Biology, Physics, and more. The primary goal is to understand how AI or LLMs (Large Language Models) interpret and organize human knowledge.

## Features

- **Interactive Visualization**: Zoom in and out to explore different periods and complexities of human knowledge.
- **Category Filtering**: Filter nodes by categories to focus on specific fields of knowledge.
- **Dynamic Annotations**: Display or hide node names based on zoom level to avoid overlap and enhance readability.
- **Hover Information**: Hover over nodes to see detailed information about each milestone.
- **Persistent Zoom Level**: Maintain the current zoom level and axis ranges when updating the figure.

## Technologies Used

- **Dash**: A Python framework for building web applications with Plotly.
- **Plotly**: A graphing library to create interactive plots.
- **Python**: The primary programming language used for this project.

## Installation

1. **Clone the Repository**

   \`\`\`bash
   git clone https://github.com/your-username/human-knowledge-timeline.git
   cd human-knowledge-timeline
   \`\`\`

2. **Create a Virtual Environment**

   \`\`\`bash
   python -m venv venv
   source venv/bin/activate   # On Windows use \`venv\Scripts\activate\`
   \`\`\`

3. **Install Dependencies**

   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Run the Application**

   \`\`\`bash
   python app.py
   \`\`\`

## Usage

- **Filtering by Category**: Use the dropdown menu to select the categories you are interested in. The graph will update to show only the selected categories.
- **Zooming and Panning**: Use your mouse or touchpad to zoom in and out or to pan across the graph. As you zoom in, more node names will appear.
- **Hover Information**: Hover over any node to see more details about that milestone in human knowledge.
- **Click for Details**: Click on a node to see detailed information about it in the panel below the graph.

## Data Structure

The data is stored in a JSON file (\`knowledge_graph.json\`) with the following structure:

\`\`\`json
{
  "nodes": [
    {
      "id": "Language",
      "category": "Communication",
      "complexity": 1.0,
      "date": "50000-01-01 BC"
    },
    ...
  ]
}
\`\`\`

- **id**: A unique identifier for the knowledge milestone.
- **category**: The field of knowledge to which this milestone belongs.
- **complexity**: A numerical value representing the complexity of the milestone.
- **date**: The date when this milestone occurred, in either BC or AD.

## Contributing

1. **Fork the Repository**
2. **Create a New Branch**

   \`\`\`bash
   git checkout -b feature/new-feature
   \`\`\`

3. **Commit Your Changes**

   \`\`\`bash
   git commit -m "Add new feature"
   \`\`\`

4. **Push to the Branch**

   \`\`\`bash
   git push origin feature/new-feature
   \`\`\`

5. **Open a Pull Request**

## License

This project is licensed under the MIT License.

## Contact

For questions or feedback, please contact [your-email@example.com].
