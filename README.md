
# 📸 Flask Image Editor (Vercel Edition)

A lightweight, serverless web application built with **Flask** and **Pillow** that allows users to upload and edit images in real-time. Designed specifically to run on **Vercel** using Serverless Functions. ⚡

---

## ✨ Features

* **📤 Fast Upload**: Upload any image format (JPG, PNG, etc.).
* **🎨 Real-time Editing**: 
    * **Brightness & Contrast**: Fine-tune the lighting.
    * **Saturation**: Make colors pop or go grayscale.
    * **Blur**: Apply Gaussian blur for soft effects.
    * **Rotation**: Rotate images up to 360 degrees.
* **💾 Instant Download**: Save your masterpiece directly to your device.
* **☁️ Serverless Optimized**: Uses `tmp` storage for fast, ephemeral processing.

---

## 🛠️ Project Structure


````

├── api/
│   └── index.py        # Main Flask backend (Serverless Entry)
├── templates/
│   └── index.html      # Frontend (HTML5 + JS)
├── vercel.json         # Vercel routing configuration
└── requirements.txt    # Python dependencies

````


## 🚀 Deployment on Vercel

1. **Push to GitHub**: Upload your files keeping the structure shown above.
2. **Connect to Vercel**: 
    * Go to [Vercel.com](https://vercel.com).
    * Import your repository.
    * Vercel will automatically detect the Python environment.
3. **Deploy**: Click **Deploy** and your app will be live in seconds! 🎉

---

## 💻 Tech Stack

* **Backend**: [Flask](https://flask.palletsprojects.com/) 🐍
* **Image Processing**: [Pillow (PIL)](https://python-pillow.org/) 🖼️
* **Frontend**: Vanilla JS & CSS3 🎨
* **Hosting**: [Vercel](https://vercel.com/) ☁️

---

## ⚠️ Important Note

Since this app runs on **Vercel Serverless Functions**, the storage is **ephemeral**. 
* Images uploaded are stored in the \`/tmp\` folder.
* Files are automatically deleted after the function execution or a short period of inactivity.
* **Always download your edited images immediately!** 📥

---

## 📝 License

Distributed under the MIT License.

---

### Made with ❤️ for developers 👨‍💻
