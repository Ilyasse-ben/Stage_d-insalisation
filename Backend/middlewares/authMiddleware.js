const jwt = require("jsonwebtoken");
const SECRET_KEY = "Mrocco_2025_CAF";

function verifyToken(req, res, next) {
  const authHeader = req.headers["authorization"];
  if (!authHeader) return res.status(403).json({ message: "Token manquant" });

  const token = authHeader.split(" ")[1];

  jwt.verify(token, SECRET_KEY, (err, user) => {
    if (err) return res.status(403).json({ message: "Token invalide ou expiré" });
    req.user = user;
    next();
  });
}

module.exports = verifyToken;
