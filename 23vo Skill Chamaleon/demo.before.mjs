// Calculate the total cost of the supplies.
const supplies = [12, 8, 5];
const total = supplies.reduce((sum, price) => sum + price, 0);
const record = { status: "ready", path: "./records/journey.json", total };

console.log("Proceso iniciado.");
if (record.status === "ready") {
  console.log(`Total: ${total}`);
} else {
  console.error("No se pudo completar el proceso.");
}

export { record };
