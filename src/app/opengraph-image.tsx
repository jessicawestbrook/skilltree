import { ImageResponse } from 'next/og'

export const runtime = 'edge'

export const alt = 'NeuroQuest - Master All Human Knowledge'
export const size = {
  width: 1200,
  height: 630,
}
export const contentType = 'image/png'

export default function OGImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'linear-gradient(135deg, #667eea, #764ba2)',
        }}
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '40px',
          }}
        >
          <div
            style={{
              fontSize: '120px',
              marginRight: '30px',
            }}
          >
            🧠
          </div>
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              color: 'white',
            }}
          >
            <div
              style={{
                fontSize: '80px',
                fontWeight: 'bold',
                letterSpacing: '-2px',
              }}
            >
              NeuroQuest
            </div>
            <div
              style={{
                fontSize: '32px',
                opacity: 0.9,
                marginTop: '10px',
              }}
            >
              Master All Human Knowledge
            </div>
          </div>
        </div>
        <div
          style={{
            display: 'flex',
            gap: '40px',
            marginTop: '40px',
          }}
        >
          {['🎨', '🔬', '💻', '🗣️', '🧮'].map((emoji, i) => (
            <div
              key={i}
              style={{
                width: '80px',
                height: '80px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: 'rgba(255, 255, 255, 0.2)',
                borderRadius: '12px',
                fontSize: '40px',
              }}
            >
              {emoji}
            </div>
          ))}
        </div>
      </div>
    ),
    {
      ...size,
    }
  )
}