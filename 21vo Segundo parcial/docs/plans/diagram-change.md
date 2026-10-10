# Requested diagram change

## Exact user request

> Ok, quiero que la categoria sean como etiquetas que se pueden agregar por lo que necesitaras un modelo de categorias y tambien una tabla intermedia para relacionar muchos a muchos.

## Changes

1. Replace `Expense.category` with `Expense.categories`, a list of tags.
2. Add the `Category` model with an identifier and a name.
3. Add the `categories` table and the `expense_categories` join table.
4. Extend `ExpenseStore` with tag creation and listing methods. Save expense
   fields and tag links together in a transaction.
5. Use a multiselect for tags when registering and editing an expense,
   alongside a small form for creating reusable tags.

## Justification

A single text field cannot represent several reusable tags. A category model
allows one tag to label many expenses. The join table also allows one expense
to have several tags without duplicating the expense or its amount.

The join table contains only two foreign keys, so an additional Python class
would add no required behavior. The three necessary classes remain `Expense`,
`Category`, and `ExpenseStore`.

## Amount allocation clarification

The assistant asked how to show an expense with several tags in the chart.
The user's exact selected answer was:

> Repartir el monto (Recomendado)

Divide integer cents equally between the expense's tags and distribute any
remaining cents in tag-identifier order. This makes the sum of the category
bars equal the sum of the filtered table, without counting the same amount
twice. Document this rule beside the chart and in the README.

## Preserved versions

- `classes-original.md`: unchanged original proposal.
- `classes-corrected.md`: corrected classes and database relationship.
