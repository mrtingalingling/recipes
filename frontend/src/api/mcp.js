/**
 * MCP Client for communicating with the MCP server.
 * 
 * Model Context Protocol allows Claude to interact with the recipes app.
 * This client calls MCP endpoints exposed by the backend.
 */

import { api } from './client';

const MCP_BASE_URL = import.meta.env.VITE_MCP_URL || 'http://localhost:8000/mcp';

export class MCPClient {
  constructor(baseUrl = MCP_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Get available MCP tools
   */
  async getTools() {
    try {
      return await api.get(`${this.baseUrl.replace('http://localhost:8000', '')}/tools`);
    } catch (error) {
      console.error('Failed to fetch MCP tools:', error);
      return { tools: [] };
    }
  }

  /**
   * Get available MCP resources
   */
  async getResources() {
    try {
      return await api.get(`${this.baseUrl.replace('http://localhost:8000', '')}/resources`);
    } catch (error) {
      console.error('Failed to fetch MCP resources:', error);
      return { resources: [] };
    }
  }

  /**
   * Call an MCP tool
   * 
   * @param {string} toolName - Name of the tool to call
   * @param {object} params - Parameters to pass to the tool
   * @returns {Promise<object>} Tool result
   */
  async callTool(toolName, params = {}) {
    try {
      return await api.post('/mcp/call', {
        tool_name: toolName,
        params,
      });
    } catch (error) {
      console.error(`MCP tool call failed: ${toolName}`, error);
      throw error;
    }
  }

  /**
   * Get MCP resource
   * 
   * @param {string} resourceUri - URI of the resource to fetch
   * @returns {Promise<object>} Resource data
   */
  async getResource(resourceUri) {
    try {
      return await api.get(`/mcp/resource`, {
        resource_uri: resourceUri,
      });
    } catch (error) {
      console.error(`Failed to fetch MCP resource: ${resourceUri}`, error);
      throw error;
    }
  }
}

// Export singleton instance
export const mcp = new MCPClient();
