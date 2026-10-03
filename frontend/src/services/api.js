const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  "http://localhost:8000";

async function parseResponse(response) {
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(
      data.detail ||
        data.message ||
        "Something went wrong while communicating with the server."
    );
  }

  return data;
}


export async function analyzeResume(
  file,
  jobDescription
) {
  const formData = new FormData();

  formData.append("file", file);
  formData.append(
    "job_description",
    jobDescription
  );

  const response = await fetch(
    `${API_BASE_URL}/api/analyze`,
    {
      method: "POST",
      body: formData,
    }
  );

  return parseResponse(response);
}


export async function uploadResume(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/api/upload-resume`,
    {
      method: "POST",
      body: formData,
    }
  );

  return parseResponse(response);
}


export async function getAIFeedback(payload) {
  const response = await fetch(
    `${API_BASE_URL}/api/ai-feedback`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    }
  );

  return parseResponse(response);
}