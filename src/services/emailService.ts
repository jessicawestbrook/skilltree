import { Resend } from 'resend';

// Initialize Resend with API key from environment (lazy initialization)
let resend: Resend | null = null;

function getResendClient(): Resend {
  if (!resend) {
    const apiKey = process.env.RESEND_API_KEY;
    if (!apiKey) {
      throw new Error('RESEND_API_KEY environment variable is not set');
    }
    resend = new Resend(apiKey);
  }
  return resend;
}

interface EmailVerificationData {
  email: string;
  username: string;
  verificationLink: string;
  token: string;
}

export async function sendVerificationEmail(data: EmailVerificationData) {
  const { email, username, verificationLink } = data;

  try {
    const resendClient = getResendClient();
    const result = await resendClient.emails.send({
      from: 'NeuroQuest <noreply@neuroquest.app>',
      to: email,
      subject: 'Verify your NeuroQuest account',
      html: getVerificationEmailTemplate(username, verificationLink),
    });

    return { success: true, data: result };
  } catch (error) {
    console.error('Failed to send verification email:', error);
    return { success: false, error };
  }
}

function getVerificationEmailTemplate(username: string, verificationLink: string): string {
  return `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verify Your Email</title>
      </head>
      <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4;">
        <table cellpadding="0" cellspacing="0" width="100%" style="background-color: #f4f4f4; padding: 20px 0;">
          <tr>
            <td align="center">
              <table cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <!-- Header -->
                <tr>
                  <td style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px 20px; text-align: center; border-radius: 10px 10px 0 0;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: bold;">NeuroQuest</h1>
                    <p style="color: #ffffff; margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Verify Your Email Address</p>
                  </td>
                </tr>

                <!-- Content -->
                <tr>
                  <td style="padding: 40px 30px;">
                    <h2 style="color: #2a2a2a; margin: 0 0 20px 0; font-size: 24px;">Welcome to NeuroQuest, ${username}!</h2>
                    
                    <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                      Thank you for joining NeuroQuest, your gateway to an extraordinary learning journey. To get started and unlock all features, please verify your email address.
                    </p>

                    <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                      Click the button below to verify your email and begin your neural adventure:
                    </p>

                    <!-- CTA Button -->
                    <table cellpadding="0" cellspacing="0" width="100%">
                      <tr>
                        <td align="center">
                          <a href="${verificationLink}" style="display: inline-block; padding: 15px 40px; background: linear-gradient(135deg, #667eea, #764ba2); color: #ffffff; text-decoration: none; border-radius: 30px; font-size: 16px; font-weight: bold; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
                            Verify Email Address
                          </a>
                        </td>
                      </tr>
                    </table>

                    <p style="color: #999999; font-size: 14px; line-height: 1.6; margin: 30px 0 0 0;">
                      If the button doesn't work, you can also copy and paste the following link into your browser:
                    </p>
                    
                    <p style="color: #667eea; font-size: 14px; line-height: 1.6; margin: 10px 0 0 0; word-break: break-all;">
                      ${verificationLink}
                    </p>

                    <div style="border-top: 1px solid #eeeeee; margin: 40px 0 20px 0; padding-top: 20px;">
                      <p style="color: #999999; font-size: 14px; line-height: 1.6; margin: 0;">
                        This verification link will expire in 24 hours. If you didn't create an account with NeuroQuest, you can safely ignore this email.
                      </p>
                    </div>
                  </td>
                </tr>

                <!-- Footer -->
                <tr>
                  <td style="background-color: #f8f9fa; padding: 30px; text-align: center; border-radius: 0 0 10px 10px;">
                    <p style="color: #999999; font-size: 14px; margin: 0 0 10px 0;">
                      Need help? Contact our support team at support@neuroquest.app
                    </p>
                    <p style="color: #999999; font-size: 12px; margin: 0;">
                      © 2024 NeuroQuest. All rights reserved.
                    </p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>
  `;
}

interface WelcomeEmailData {
  email: string;
  username: string;
}

export async function sendWelcomeEmail(data: WelcomeEmailData) {
  const { email, username } = data;

  try {
    const resendClient = getResendClient();
    const result = await resendClient.emails.send({
      from: 'NeuroQuest <noreply@neuroquest.app>',
      to: email,
      subject: 'Welcome to NeuroQuest - Your Learning Journey Begins!',
      html: getWelcomeEmailTemplate(username),
    });

    return { success: true, data: result };
  } catch (error) {
    console.error('Failed to send welcome email:', error);
    return { success: false, error };
  }
}

function getWelcomeEmailTemplate(username: string): string {
  return `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to NeuroQuest</title>
      </head>
      <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4;">
        <table cellpadding="0" cellspacing="0" width="100%" style="background-color: #f4f4f4; padding: 20px 0;">
          <tr>
            <td align="center">
              <table cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <!-- Header -->
                <tr>
                  <td style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px 20px; text-align: center; border-radius: 10px 10px 0 0;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: bold;">Welcome to NeuroQuest!</h1>
                    <p style="color: #ffffff; margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Your learning adventure begins now</p>
                  </td>
                </tr>

                <!-- Content -->
                <tr>
                  <td style="padding: 40px 30px;">
                    <h2 style="color: #2a2a2a; margin: 0 0 20px 0; font-size: 24px;">Congratulations, ${username}!</h2>
                    
                    <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                      Your email has been verified successfully! You're now ready to embark on an incredible journey of knowledge and discovery.
                    </p>

                    <h3 style="color: #2a2a2a; margin: 30px 0 15px 0; font-size: 18px;">🚀 Here's what you can do next:</h3>
                    
                    <ul style="color: #666666; font-size: 16px; line-height: 1.8; margin: 0 0 30px 0; padding-left: 20px;">
                      <li>Explore our interactive knowledge graph</li>
                      <li>Start your first learning path</li>
                      <li>Complete challenges and earn achievements</li>
                      <li>Connect with other learners</li>
                      <li>Track your progress and level up</li>
                    </ul>

                    <!-- CTA Button -->
                    <table cellpadding="0" cellspacing="0" width="100%">
                      <tr>
                        <td align="center">
                          <a href="${process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'}" style="display: inline-block; padding: 15px 40px; background: linear-gradient(135deg, #667eea, #764ba2); color: #ffffff; text-decoration: none; border-radius: 30px; font-size: 16px; font-weight: bold; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
                            Start Learning Now
                          </a>
                        </td>
                      </tr>
                    </table>

                    <div style="background-color: #f8f9fa; border-radius: 8px; padding: 20px; margin: 40px 0 0 0;">
                      <h4 style="color: #2a2a2a; margin: 0 0 10px 0; font-size: 16px;">💡 Pro Tip:</h4>
                      <p style="color: #666666; font-size: 14px; line-height: 1.6; margin: 0;">
                        Start with the "Fundamentals" learning path to build a strong foundation. Each completed node brings you closer to becoming a Neural Master!
                      </p>
                    </div>
                  </td>
                </tr>

                <!-- Footer -->
                <tr>
                  <td style="background-color: #f8f9fa; padding: 30px; text-align: center; border-radius: 0 0 10px 10px;">
                    <p style="color: #999999; font-size: 14px; margin: 0 0 10px 0;">
                      Questions? We're here to help at support@neuroquest.app
                    </p>
                    <p style="color: #999999; font-size: 12px; margin: 0;">
                      © 2024 NeuroQuest. All rights reserved.
                    </p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>
  `;
}