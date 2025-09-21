import React, { useState, useEffect } from 'react';
import {
  Shield,
  Smartphone,
  Mail,
  Key,
  CheckCircle,
  AlertTriangle,
  RefreshCw
} from 'lucide-react';
import { mfaAPI } from '../../services/api';
import toast from 'react-hot-toast';

const MFAVerification = ({ userId, userEmail, onSuccess, onCancel }) => {
  const [method, setMethod] = useState('totp'); // totp, email
  const [totpCode, setTotpCode] = useState('');
  const [emailCode, setEmailCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [emailSent, setEmailSent] = useState(false);
  const [timeLeft, setTimeLeft] = useState(0);

  useEffect(() => {
    if (method === 'email' && !emailSent) {
      sendEmailVerification();
    }
  }, [method]);

  useEffect(() => {
    if (timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [timeLeft]);

  const sendEmailVerification = async () => {
    setIsLoading(true);
    try {
      const response = await mfaAPI.sendEmailVerification(userId, userEmail);
      if (response.success) {
        setEmailSent(true);
        setTimeLeft(600); // 10 minutes
        toast.success('Verification email sent!');
      } else {
        toast.error(response.message || 'Failed to send verification email');
      }
    } catch (error) {
      toast.error('Failed to send verification email');
    } finally {
      setIsLoading(false);
    }
  };

  const verifyTOTP = async () => {
    if (!totpCode || totpCode.length !== 6) {
      toast.error('Please enter a 6-digit code');
      return;
    }

    setIsLoading(true);
    try {
      const response = await mfaAPI.verifySetup(userId, totpCode);
      if (response.success) {
        onSuccess && onSuccess();
      } else {
        toast.error(response.message || 'Invalid verification code');
        setTotpCode('');
      }
    } catch (error) {
      toast.error('Failed to verify code');
    } finally {
      setIsLoading(false);
    }
  };

  const verifyEmail = async () => {
    if (!emailCode || emailCode.length !== 6) {
      toast.error('Please enter a 6-digit code');
      return;
    }

    setIsLoading(true);
    try {
      const response = await mfaAPI.verifyEmailCode(userId, emailCode);
      if (response.success) {
        onSuccess && onSuccess();
      } else {
        toast.error(response.message || 'Invalid verification code');
        setEmailCode('');
      }
    } catch (error) {
      toast.error('Failed to verify code');
    } finally {
      setIsLoading(false);
    }
  };

  const resendEmail = () => {
    setEmailSent(false);
    setEmailCode('');
    sendEmailVerification();
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-6">
      <div className="text-center mb-6">
        <div className="flex justify-center mb-4">
          <div className="p-3 bg-blue-100 rounded-full">
            <Shield className="h-8 w-8 text-blue-600" />
          </div>
        </div>
        <h2 className="text-xl font-semibold text-gray-900 mb-2">
          Multi-Factor Authentication
        </h2>
        <p className="text-gray-600">
          Please verify your identity to continue
        </p>
      </div>

      {/* Method Selection */}
      <div className="mb-6">
        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
          <button
            onClick={() => setMethod('totp')}
            className={`flex-1 flex items-center justify-center px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              method === 'totp'
                ? 'bg-white text-blue-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Smartphone className="h-4 w-4 mr-2" />
            Authenticator App
          </button>
          <button
            onClick={() => setMethod('email')}
            className={`flex-1 flex items-center justify-center px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              method === 'email'
                ? 'bg-white text-blue-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Mail className="h-4 w-4 mr-2" />
            Email Code
          </button>
        </div>
      </div>

      {/* TOTP Verification */}
      {method === 'totp' && (
        <div className="space-y-4">
          <div className="text-center">
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Enter Authenticator Code
            </h3>
            <p className="text-sm text-gray-600">
              Open your authenticator app and enter the 6-digit code
            </p>
          </div>

          <div>
            <input
              type="text"
              value={totpCode}
              onChange={(e) => setTotpCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
              placeholder="000000"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-center text-2xl tracking-widest font-mono"
              maxLength={6}
            />
          </div>

          <button
            onClick={verifyTOTP}
            disabled={isLoading || totpCode.length !== 6}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Verifying...' : 'Verify Code'}
          </button>
        </div>
      )}

      {/* Email Verification */}
      {method === 'email' && (
        <div className="space-y-4">
          <div className="text-center">
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Enter Email Code
            </h3>
            <p className="text-sm text-gray-600">
              We sent a 6-digit code to {userEmail}
            </p>
          </div>

          {emailSent && timeLeft > 0 && (
            <div className="bg-blue-50 border border-blue-200 rounded-md p-3">
              <div className="flex items-center">
                <Mail className="h-4 w-4 text-blue-400 mr-2" />
                <span className="text-sm text-blue-700">
                  Code expires in {formatTime(timeLeft)}
                </span>
              </div>
            </div>
          )}

          <div>
            <input
              type="text"
              value={emailCode}
              onChange={(e) => setEmailCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
              placeholder="000000"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-center text-2xl tracking-widest font-mono"
              maxLength={6}
            />
          </div>

          <div className="flex space-x-3">
            <button
              onClick={resendEmail}
              disabled={isLoading || timeLeft > 0}
              className="flex-1 px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Sending...' : 'Resend Code'}
            </button>
            <button
              onClick={verifyEmail}
              disabled={isLoading || emailCode.length !== 6}
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Verifying...' : 'Verify Code'}
            </button>
          </div>
        </div>
      )}

      {/* Security Notice */}
      <div className="mt-6 bg-yellow-50 border border-yellow-200 rounded-md p-4">
        <div className="flex">
          <AlertTriangle className="h-5 w-5 text-yellow-400" />
          <div className="ml-3">
            <h4 className="text-sm font-medium text-yellow-800">
              Security Notice
            </h4>
            <p className="mt-1 text-sm text-yellow-700">
              Never share your verification codes with anyone. IT Support Pro will never ask for your MFA codes.
            </p>
          </div>
        </div>
      </div>

      {/* Cancel Button */}
      <div className="mt-4 text-center">
        <button
          onClick={onCancel}
          className="text-sm text-gray-600 hover:text-gray-900"
        >
          Cancel and go back
        </button>
      </div>
    </div>
  );
};

export default MFAVerification;




