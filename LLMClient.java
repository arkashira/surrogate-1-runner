@Test
void testGetResponse() {
    String result = client.getResponse("LLM_PROVIDER", "Hello world");
    assertNotNull(result);
}