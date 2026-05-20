import AnomalyDetector from './anomaly-detection';

describe('AnomalyDetector', () => {
  it('detects anomalies', () => {
    const ad = new AnomalyDetector(2);
    ad.addData({ date: '2022-01-01', cost: 100 });
    ad.addData({ date: '2022-01-02', cost: 150 });
    ad.addData({ date: '2022-01-03', cost: 10000 }); // Anomaly
    ad.addData({ date: '2022-01-04', cost: 200 });

    expect(ad.detectAnomalies()).toEqual([
      { date: '2022-01-03', cost: 10000 }
    ]);
  });
});