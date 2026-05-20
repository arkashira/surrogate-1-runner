import React from 'react';
import CostService from '../services/costService';

class CostMetrics extends React.Component {
  state = {
    costData: [],
  };

  componentDidMount() {
    this.fetchCostData();
  }

  fetchCostData = async () => {
    const costService = new CostService();
    const costData = await costService.getCostData('PROJECT_ID', 'RESOURCE_TYPE');
    this.setState({ costData });
  };

  render() {
    return (
      <div>
        <h1>Cost Metrics</h1>
        <ul>
          {this.state.costData.map((item, index) => (
            <li key={index}>{item.cost}</li>
          ))}
        </ul>
      </div>
    );
  }
}

export default CostMetrics;