using System.Net.Http.Json;
using ModelContextProtocol.Server;

namespace OntologyMcp;

[McpServerToolType]
public static class OntologyTools
{
    private static readonly HttpClient client = new();

    [McpServerTool]
    public static async Task<object> SearchOntology(string question)
    {
        var response = await client.PostAsJsonAsync(
            "http://127.0.0.1:8000/search",
            new
            {
                question = question
            });

        response.EnsureSuccessStatusCode();

        return await response.Content.ReadFromJsonAsync<object>();
    }
}