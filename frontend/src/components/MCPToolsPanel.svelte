/**
 * Example Svelte component showing MCP integration
 * 
 * Demonstrates:
 * - Calling MCP tools from frontend
 * - Handling MCP responses
 * - Loading states for long operations
 */

<script>
  import { mcp } from '../api/mcp.js';
  import { loadingStates, errorStates } from '../stores/app.js';
  import { setLoading, setError, clearError } from '../stores/app.js';

  let availableTools = [];
  let selectedTool = null;
  let toolParams = {};
  let toolResult = null;

  async function loadTools() {
    setLoading('mcp', true);
    try {
      const response = await mcp.getTools();
      availableTools = Object.entries(response.data || response.tools || {}).map(
        ([name, schema]) => ({
          name,
          schema,
        })
      );
    } catch (error) {
      setError('mcp', error.message);
    } finally {
      setLoading('mcp', false);
    }
  }

  async function callSelectedTool() {
    if (!selectedTool) return;

    setLoading('mcp', true);
    clearError('mcp');
    try {
      const result = await mcp.callTool(selectedTool.name, toolParams);
      toolResult = result;
    } catch (error) {
      setError('mcp', error.message);
      toolResult = null;
    } finally {
      setLoading('mcp', false);
    }
  }

  function selectTool(tool) {
    selectedTool = tool;
    toolParams = {};
    toolResult = null;
  }

  function updateParam(paramName, value) {
    toolParams[paramName] = value;
  }

  onMount(loadTools);
</script>

<div class="mcp-integration">
  <h2>MCP Tools (Claude Integration)</h2>

  {#if $loadingStates.mcp}
    <div class="loading">Loading MCP tools...</div>
  {:else if $errorStates.mcp}
    <div class="error">
      Error: {$errorStates.mcp}
      <button on:click={loadTools}>Retry</button>
    </div>
  {:else}
    <div class="tools-section">
      <h3>Available Tools</h3>
      <div class="tools-list">
        {#each availableTools as tool (tool.name)}
          <button
            class:selected={selectedTool?.name === tool.name}
            on:click={() => selectTool(tool)}
          >
            {tool.name}
          </button>
        {/each}
      </div>

      {#if selectedTool}
        <div class="tool-detail">
          <h4>{selectedTool.name}</h4>
          <p>{selectedTool.schema.description}</p>

          <div class="params-form">
            <h5>Parameters</h5>
            {#each Object.entries(selectedTool.schema.inputSchema?.properties || {}) as [paramName, paramSchema]}
              <div class="param-input">
                <label for={paramName}>
                  {paramName}
                  {#if selectedTool.schema.inputSchema?.required?.includes(paramName)}
                    <span class="required">*</span>
                  {/if}
                </label>

                {#if paramSchema.type === 'string'}
                  {#if paramSchema.enum}
                    <select
                      id={paramName}
                      on:change={e => updateParam(paramName, e.target.value)}
                    >
                      <option value="">Select...</option>
                      {#each paramSchema.enum as option}
                        <option value={option}>{option}</option>
                      {/each}
                    </select>
                  {:else}
                    <input
                      id={paramName}
                      type="text"
                      placeholder={paramSchema.description}
                      on:change={e => updateParam(paramName, e.target.value)}
                    />
                  {/if}
                {:else if paramSchema.type === 'number'}
                  <input
                    id={paramName}
                    type="number"
                    placeholder={paramSchema.description}
                    on:change={e => updateParam(paramName, parseFloat(e.target.value))}
                  />
                {:else if paramSchema.type === 'array'}
                  <input
                    id={paramName}
                    type="text"
                    placeholder="Comma-separated values"
                    on:change={e => updateParam(paramName, e.target.value.split(','))}
                  />
                {/if}
              </div>
            {/each}
          </div>

          <button on:click={callSelectedTool} disabled={$loadingStates.mcp}>
            {$loadingStates.mcp ? 'Executing...' : 'Execute Tool'}
          </button>

          {#if toolResult}
            <div class="result">
              <h5>Result</h5>
              <pre>{JSON.stringify(toolResult, null, 2)}</pre>
            </div>
          {/if}
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .mcp-integration {
    padding: 20px;
    background: #f9f9f9;
    border-radius: 8px;
    margin: 20px 0;
  }

  h2 {
    color: #333;
    border-bottom: 2px solid #007bff;
    margin-top: 0;
  }

  .tools-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 15px 0;
  }

  .tools-list button {
    padding: 8px 12px;
    border: 1px solid #ddd;
    background: white;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .tools-list button:hover {
    background: #f0f0f0;
  }

  .tools-list button.selected {
    background: #007bff;
    color: white;
    border-color: #007bff;
  }

  .tool-detail {
    margin-top: 20px;
    padding: 15px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  .tool-detail h4 {
    margin-top: 0;
    color: #333;
  }

  .params-form {
    margin: 15px 0;
  }

  .param-input {
    margin: 10px 0;
    display: flex;
    flex-direction: column;
  }

  .param-input label {
    font-weight: 500;
    margin-bottom: 5px;
    color: #555;
  }

  .required {
    color: #d32f2f;
  }

  .param-input input,
  .param-input select {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-family: inherit;
  }

  .result {
    margin-top: 15px;
    padding: 15px;
    background: #e8f5e9;
    border-radius: 4px;
    border-left: 4px solid #4caf50;
  }

  .result pre {
    margin: 0;
    overflow-x: auto;
    background: white;
    padding: 10px;
    border-radius: 4px;
    font-size: 12px;
  }

  .loading,
  .error {
    padding: 15px;
    border-radius: 4px;
    margin: 15px 0;
  }

  .loading {
    background: #e3f2fd;
    color: #1d64a1;
  }

  .error {
    background: #ffebee;
    color: #c62828;
  }

  .error button {
    margin-top: 10px;
    padding: 6px 12px;
    background: #c62828;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
</style>
