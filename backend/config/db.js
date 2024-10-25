import mongoose from "mongoose";
import 'dotenv/config'; // Ensure that the .env file is loaded

export const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log("Database Connected");
  } catch (error) {
    console.error("Database connection failed:", error.message);
    process.exit(1); // Exit the process with a failure code
  }
};
