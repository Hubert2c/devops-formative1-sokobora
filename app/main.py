"""
Soko Bora - Agricultural Market Price Tracker
Main application entry point.

Core feature (F1 requirement: "demonstrate at least one core feature"):
Farmers and buyers can submit and view crop prices reported at specific
markets, so smallholder farmers can compare prices across markets before
selling their produce.
"""

import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    """Application factory - makes it easy to create isolated app
    instances for testing vs. running the real server."""
    app = Flask(__name__)

    default_db_uri = os.environ.get(
        "DATABASE_URL", "sqlite:///soko_bora.db"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = default_db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)
    return app


class PriceEntry(db.Model):
    """A single reported price for a crop at a specific market."""

    __tablename__ = "price_entries"

    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    market_name = db.Column(db.String(150), nullable=False)
    region = db.Column(db.String(150), nullable=False)
    price_per_kg = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False, default="RWF")
    reported_by = db.Column(db.String(150), nullable=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return {
            "id": self.id,
            "crop_name": self.crop_name,
            "market_name": self.market_name,
            "region": self.region,
            "price_per_kg": self.price_per_kg,
            "currency": self.currency,
            "reported_by": self.reported_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


def register_routes(app):

    @app.route("/")
    def index():
        return jsonify({
            "message": "Soko Bora - Agricultural Market Price Tracker API",
            "status": "running",
        })

    @app.route("/health")
    def health():
        """Health check endpoint used by Docker/CI/orchestration tools."""
        return jsonify({"status": "healthy"}), 200

    @app.route("/api/prices", methods=["POST"])
    def create_price():
        """Submit a new crop price report.

        Expected JSON body:
        {
            "crop_name": "Maize",
            "market_name": "Kimironko Market",
            "region": "Kigali",
            "price_per_kg": 350,
            "currency": "RWF",
            "reported_by": "farmer_jane"
        }
        """
        data = request.get_json(silent=True) or {}

        required_fields = ["crop_name", "market_name", "region", "price_per_kg"]
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({
                "error": f"Missing required field(s): {', '.join(missing)}"
            }), 400

        try:
            price_value = float(data["price_per_kg"])
        except (TypeError, ValueError):
            return jsonify({"error": "price_per_kg must be a number"}), 400

        entry = PriceEntry(
            crop_name=data["crop_name"],
            market_name=data["market_name"],
            region=data["region"],
            price_per_kg=price_value,
            currency=data.get("currency", "RWF"),
            reported_by=data.get("reported_by"),
        )
        db.session.add(entry)
        db.session.commit()

        return jsonify(entry.to_dict()), 201

    @app.route("/api/prices", methods=["GET"])
    def list_prices():
        """List crop price reports, optionally filtered by crop or region.

        Query params:
            crop_name (optional)
            region (optional)
        """
        query = PriceEntry.query

        crop_name = request.args.get("crop_name")
        if crop_name:
            query = query.filter(PriceEntry.crop_name.ilike(f"%{crop_name}%"))

        region = request.args.get("region")
        if region:
            query = query.filter(PriceEntry.region.ilike(f"%{region}%"))

        entries = query.order_by(PriceEntry.created_at.desc()).all()
        return jsonify([e.to_dict() for e in entries]), 200


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
