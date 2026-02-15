# API Request Examples

## Example 1: Generate Leads for Cafes

### Request
```bash
curl -X POST "http://localhost:8000/generate-leads" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "best cafes in bhopal",
    "max_results": 5
  }'
```

### Response
```json
{
  "success": true,
  "message": "Successfully generated 5 leads",
  "total_leads": 5,
  "leads": [
    {
      "business_name": "Cafe Coffee Day",
      "owner_name": "",
      "rating": "4.2",
      "website": "https://www.cafecoffeeday.com",
      "email": "contact@cafecoffeeday.com",
      "opening_hours": "8:00 AM - 11:00 PM",
      "website_exists": true,
      "cold_email": "Hi,\n\nI came across Cafe Coffee Day and was impressed by your 4.2 rating..."
    }
  ],
  "saved_to_sheets": true
}
```

## Example 2: Generate Leads for Restaurants

### Request
```bash
curl -X POST "http://localhost:8000/generate-leads" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "top restaurants in mumbai",
    "max_results": 10
  }'
```

## Example 3: Generate Leads for Gyms

### Request
```bash
curl -X POST "http://localhost:8000/generate-leads" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "best gyms in delhi",
    "max_results": 8
  }'
```

## Example 4: Send Cold Emails

### Request
```bash
curl -X POST "http://localhost:8000/send-emails" \
  -H "Content-Type: application/json" \
  -d '{
    "leads": [
      {
        "email": "contact@example.com",
        "cold_email": "Hi,\n\nI noticed your business..."
      }
    ],
    "subject": "Website Improvement Opportunity"
  }'
```

### Response
```json
{
  "success": true,
  "sent": 1,
  "failed": 0,
  "errors": []
}
```

## Example 5: Health Check

### Request
```bash
curl http://localhost:8000/health
```

### Response
```json
{
  "status": "healthy",
  "services": {
    "api": "online",
    "openai": "configured",
    "serper": "configured",
    "google_sheets": "configured",
    "smtp": "configured"
  }
}
```

## Python Example

```python
import requests

# Generate leads
response = requests.post(
    "http://localhost:8000/generate-leads",
    json={
        "query": "best cafes in bhopal",
        "max_results": 10
    }
)

data = response.json()

if data["success"]:
    print(f"Generated {data['total_leads']} leads")
    
    for lead in data["leads"]:
        print(f"\nBusiness: {lead['business_name']}")
        print(f"Email: {lead['email']}")
        print(f"Rating: {lead['rating']}")
```

## JavaScript Example

```javascript
// Generate leads
const response = await fetch('http://localhost:8000/generate-leads', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        query: 'best cafes in bhopal',
        max_results: 10
    })
});

const data = await response.json();

if (data.success) {
    console.log(`Generated ${data.total_leads} leads`);
    
    data.leads.forEach(lead => {
        console.log(`\nBusiness: ${lead.business_name}`);
        console.log(`Email: ${lead.email}`);
        console.log(`Rating: ${lead.rating}`);
    });
}
```
