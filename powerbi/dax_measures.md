# Power BI measures

The `.pbix` report (`sales-data-analysis.pbix`) mirrors the Python pipeline in
`src/`. This file documents the DAX measures so the logic is reviewable without
opening Power BI.

## Expected model

- **FactSales** — one row per order (`Sheet3`).
- **DimProduct** — product dimension keyed on `ProductID`.
- **DimCustomer** — customer dimension keyed on `Customer ID`.
- **DimPromotion** — promotion dimension keyed on `PromotionID`.

Sales and profit are derived in the model from `Units Sold`, the product price,
and the promotion discount, because the source fact table does not carry cost.

## Measures

```dax
Total Sales =
SUMX ( FactSales, FactSales[Units Sold] * RELATED ( DimProduct[Price (INR)] ) )

Discount % =
VAR Terms = SELECTEDVALUE ( DimPromotion[Price Reduction Type] )
RETURN
    SWITCH (
        TRUE (),
        CONTAINSSTRING ( Terms, "Buy 1 Get 1" ), 0.50,
        CONTAINSSTRING ( Terms, "%" ),
            DIVIDE ( VALUE ( SUBSTITUTE ( Terms, "% off", "" ) ), 100 ),
        0
    )

Discount Value = [Total Sales] * [Discount %]

Net Sales = [Total Sales] - [Discount Value]

Profit Margin = 0.10   -- flat margin assumption (no cost column in source data)

Total Profit = [Net Sales] * [Profit Margin]

Total Quantity = SUM ( FactSales[Units Sold] )

Total Orders = COUNTROWS ( FactSales )

Average Discount % = AVERAGEX ( DimPromotion, [Discount %] )
```

## Assumptions

- Discount is parsed from each promotion's terms; `Buy 1 Get 1 Free` is modeled
  as an effective 50% discount.
- Profit uses a flat 10% margin on net sales, matching `src/config.py`.
- Orders without a promotion are labeled `No Promotion` and carry a 0% discount.
