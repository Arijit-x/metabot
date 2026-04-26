# Mock OpenMetadata client — works without sandbox login
# Perfect for demo purposes

MOCK_TABLES = [
    {
        "id": "1",
        "name": "dim_customer",
        "fullyQualifiedName": "sample_data.ecommerce_db.shopify.dim_customer",
        "description": "Customer dimension table with PII data including name, email and address.",
        "owner": "Data Engineering Team",
        "tags": ["PII", "Sensitive"],
        "columns": [
            {"name": "customer_id", "dataType": "INT", "description": "Unique customer ID"},
            {"name": "name", "dataType": "VARCHAR", "description": "Full name of customer"},
            {"name": "email", "dataType": "VARCHAR", "description": "Customer email (PII)"},
            {"name": "phone", "dataType": "VARCHAR", "description": "Phone number (PII)"},
            {"name": "address", "dataType": "TEXT", "description": "Shipping address"},
            {"name": "created_at", "dataType": "TIMESTAMP", "description": "Account creation date"},
        ],
    },
    {
        "id": "2",
        "name": "fact_order",
        "fullyQualifiedName": "sample_data.ecommerce_db.shopify.fact_order",
        "description": "Order fact table containing all transaction records.",
        "owner": "Analytics Team",
        "tags": ["Finance", "Critical"],
        "columns": [
            {"name": "order_id", "dataType": "INT", "description": "Unique order ID"},
            {"name": "customer_id", "dataType": "INT", "description": "FK to dim_customer"},
            {"name": "amount", "dataType": "DECIMAL", "description": "Order total amount"},
            {"name": "status", "dataType": "VARCHAR", "description": "Order status"},
            {"name": "order_date", "dataType": "TIMESTAMP", "description": "Order placed date"},
        ],
    },
    {
        "id": "3",
        "name": "dim_product",
        "fullyQualifiedName": "sample_data.ecommerce_db.shopify.dim_product",
        "description": "Product catalog with pricing and category info.",
        "owner": "Product Team",
        "tags": ["Catalog"],
        "columns": [
            {"name": "product_id", "dataType": "INT", "description": "Unique product ID"},
            {"name": "name", "dataType": "VARCHAR", "description": "Product name"},
            {"name": "price", "dataType": "DECIMAL", "description": "Unit price"},
            {"name": "category", "dataType": "VARCHAR", "description": "Product category"},
        ],
    },
    {
        "id": "4",
        "name": "raw_orders",
        "fullyQualifiedName": "sample_data.ecommerce_db.shopify.raw_orders",
        "description": "Raw orders ingested from Shopify API.",
        "owner": "Data Engineering Team",
        "tags": ["Raw", "Ingestion"],
        "columns": [
            {"name": "id", "dataType": "INT", "description": "Raw order ID"},
            {"name": "payload", "dataType": "JSON", "description": "Full order JSON payload"},
            {"name": "ingested_at", "dataType": "TIMESTAMP", "description": "Ingestion timestamp"},
        ],
    },
    {
        "id": "5",
        "name": "revenue_dashboard",
        "fullyQualifiedName": "sample_data.ecommerce_db.shopify.revenue_dashboard",
        "description": "Aggregated revenue metrics used in dashboards.",
        "owner": "BI Team",
        "tags": ["Dashboard", "Finance"],
        "columns": [
            {"name": "date", "dataType": "DATE", "description": "Revenue date"},
            {"name": "total_revenue", "dataType": "DECIMAL", "description": "Total daily revenue"},
            {"name": "order_count", "dataType": "INT", "description": "Number of orders"},
        ],
    },
]


class OpenMetadataClient:
    def __init__(self, base_url: str = "", token: str = ""):
        print("[MetaBot] ✅ Using mock data — no sandbox login needed!")

    def search_tables(self, query: str):
        query = query.lower()
        results = []
        for t in MOCK_TABLES:
            if (query in t["name"].lower() or
                query in t["description"].lower() or
                any(query in tag.lower() for tag in t["tags"]) or
                query in t["owner"].lower()):
                results.append({
                    "id": t["id"],
                    "name": t["name"],
                    "fullyQualifiedName": t["fullyQualifiedName"],
                    "description": t["description"],
                    "owner": t["owner"],
                    "tags": t["tags"],
                })
        return results if results else [{"message": f"No tables found for '{query}'"}]

    def get_table_details(self, table_fqn: str):
        for t in MOCK_TABLES:
            if t["fullyQualifiedName"] == table_fqn or t["name"] in table_fqn:
                return t
        return {"error": f"Table '{table_fqn}' not found"}

    def get_table_owner(self, table_fqn: str):
        details = self.get_table_details(table_fqn)
        if "error" in details:
            return details
        return {"owner": details.get("owner", "Unknown")}

    def get_lineage(self, table_fqn: str):
        lineage_map = {
            "fact_order": {
                "nodes": [
                    {"name": "raw_orders", "type": "upstream"},
                    {"name": "dim_customer", "type": "upstream"},
                    {"name": "revenue_dashboard", "type": "downstream"},
                ],
                "edges": [
                    {"from": "raw_orders", "to": "fact_order"},
                    {"from": "dim_customer", "to": "fact_order"},
                    {"from": "fact_order", "to": "revenue_dashboard"},
                ],
            },
            "revenue_dashboard": {
                "nodes": [{"name": "fact_order", "type": "upstream"}],
                "edges": [{"from": "fact_order", "to": "revenue_dashboard"}],
            },
        }
        for key, lineage in lineage_map.items():
            if key in table_fqn:
                return lineage
        return {"nodes": [], "edges": [], "message": "No lineage found for this table"}

    def list_recently_updated(self):
        import datetime
        now = datetime.datetime.now()
        return [
            {
                "name": t["name"],
                "fullyQualifiedName": t["fullyQualifiedName"],
                "updatedAt": (now - datetime.timedelta(hours=i * 3)).isoformat(),
                "owner": t["owner"],
            }
            for i, t in enumerate(MOCK_TABLES)
        ]
