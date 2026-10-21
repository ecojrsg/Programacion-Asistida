// Reckon here the full cost of our provisions.
const supplies = [12, 8, 5];
const total = supplies.reduce((sum, price) => sum + price, 0);
const record = { status: "ready", path: "./records/journey.json", total };

console.log("Doy comienzo a esta jornada.");
if (record.status === "ready") {
  console.log(`Que conste en esta crónica el total: ${total}`);
} else {
  console.error("No me fue posible llevar esta jornada a término.");
}

export { record };
