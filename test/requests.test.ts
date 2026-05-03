test('GET /requests?overdue=true returns only overdue', async () => {
  const res = await request(app).get('/requests?overdue=true');
  expect(res.status).toBe(200);
  expect(res.body.requests.every((r: any) => r.overdue)).toBe(true);
  expect(res.body.overdue_count).toBe(res.body.requests.length);
});