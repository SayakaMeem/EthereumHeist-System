<h2>🧪 Software Testing and Quality Assurance</h2>

<p>
The EthereumHeist AML System was validated through professional manual QA practices
to ensure functional correctness, API reliability, database consistency, and stable
frontend-backend communication.
</p>

<h3>🎯 Testing Objectives</h3>

<ul>
<li>Verify that all major application workflows work according to requirements.</li>
<li>Validate transaction tracking and AML analysis functionality.</li>
<li>Ensure API responses are accurate and reliable.</li>
<li>Verify database consistency and data integrity.</li>
<li>Identify, document, and track software defects.</li>
<li>Ensure system stability after updates through regression testing.</li>
</ul>


<h3>✅ Testing Activities Performed</h3>

<table>
<tr>
<th>Testing Type</th>
<th>Description</th>
</tr>

<tr>
<td>Functional Testing</td>
<td>
Verified core features including Ethereum address analysis,
multi-hop transaction tracking, risk scoring, service matching,
graph generation, and evidence export.
</td>
</tr>

<tr>
<td>Regression Testing</td>
<td>
Retested existing functionality after updates to ensure new changes
did not break previously working modules.
</td>
</tr>

<tr>
<td>API Testing</td>
<td>
Validated REST API endpoints, request parameters, response formats,
successful responses, and error handling using Postman.
</td>
</tr>

<tr>
<td>Database Testing</td>
<td>
Checked transaction storage, retrieval accuracy, data consistency,
and validation of generated investigation records.
</td>
</tr>

<tr>
<td>Error Handling Testing</td>
<td>
Tested invalid inputs, missing parameters, unavailable resources,
and unexpected system behavior.
</td>
</tr>

<tr>
<td>Input Validation Testing</td>
<td>
Verified correct handling of valid and invalid Ethereum addresses,
parameters, and user inputs.
</td>
</tr>

</table>


<h3>🧪 Testing Scope</h3>

<table>

<tr>
<th>Module</th>
<th>Testing Performed</th>
</tr>

<tr>
<td>Frontend Dashboard</td>
<td>
UI workflow testing, data display validation,
API response rendering, and user interaction testing.
</td>
</tr>

<tr>
<td>FastAPI Backend</td>
<td>
Endpoint testing, request validation,
response verification, and error handling.
</td>
</tr>

<tr>
<td>Transaction Tracking Engine</td>
<td>
Validation of one-hop and multi-hop fund tracking,
layer generation, and edge creation.
</td>
</tr>

<tr>
<td>Risk Scoring Module</td>
<td>
Verification of risk score calculation,
risk levels, and suspicious transaction labeling.
</td>
</tr>

<tr>
<td>Evidence Generation</td>
<td>
Validation of CSV, JSON summaries,
and downloadable investigation outputs.
</td>
</tr>

</table>


<h3>🛠️ Testing Tools</h3>

<table>

<tr>
<th>Tool</th>
<th>Purpose</th>
</tr>

<tr>
<td>Postman</td>
<td>REST API testing and response validation</td>
</tr>

<tr>
<td>SQL</td>
<td>Database validation and data integrity checking</td>
</tr>

<tr>
<td>Browser Developer Tools</td>
<td>Frontend debugging and network inspection</td>
</tr>

<tr>
<td>Jira</td>
<td>Bug tracking and defect management</td>
</tr>

</table>


<h3>📋 QA Documentation</h3>

<p>
Complete testing documentation is available in the 
<code>/testing</code> directory.
</p>

<pre>
testing/
│
├── Test_Plan.md
├── Functional_Test_Cases.xlsx
├── API_Testing.md
├── Database_Testing.md
├── Bug_Report.md
├── Regression_Test_Report.md
├── Test_Data.md
└── Test_Summary.md
</pre>


<h3>🐞 Defect Reporting Process</h3>

<p>
Detected issues were documented using professional bug reporting practices.
Each defect report contains:
</p>

<ul>
<li>Bug ID</li>
<li>Bug Description</li>
<li>Environment Details</li>
<li>Steps to Reproduce</li>
<li>Expected Result</li>
<li>Actual Result</li>
<li>Severity Level</li>
<li>Priority Level</li>
<li>Resolution Status</li>
</ul>


<h3>📊 Testing Result</h3>

<table>

<tr>
<th>Testing Category</th>
<th>Status</th>
</tr>

<tr>
<td>Functional Testing</td>
<td>✅ Passed</td>
</tr>

<tr>
<td>API Testing</td>
<td>✅ Passed</td>
</tr>

<tr>
<td>Database Testing</td>
<td>✅ Passed</td>
</tr>

<tr>
<td>Regression Testing</td>
<td>✅ Passed</td>
</tr>

<tr>
<td>Error Handling Testing</td>
<td>✅ Passed</td>
</tr>

</table>


<p>
The testing process confirmed that the EthereumHeist AML System
maintains reliable functionality across its core investigation,
analysis, and evidence-generation workflows.
</p>
