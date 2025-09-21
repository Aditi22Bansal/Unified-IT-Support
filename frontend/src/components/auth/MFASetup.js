import React, { useState, useEffect } from 'react';
import {
  Shield,
  QrCode,
  CheckCircle,
  AlertTriangle,
  Smartphone,
  Mail,
  Key
} from 'lucide-react';
import { mfaAPI } from '../../services/api';
import toast from 'react-hot-toast';

const MFASetup = ({ userId, userEmail, onComplete }) => {
  const [step, setStep] = useState('setup'); // setup, verify, complete
  const [qrCodeUrl, setQrCodeUrl] = useState('');
  const [verificationToken, setVerificationToken] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [mfaStatus, setMfaStatus] = useState(null);

  useEffect(() => {
    checkMfaStatus();
  }, [userId]);

  const checkMfaStatus = async () => {
    try {
      const response = await mfaAPI.getStatus(userId);
      setMfaStatus(response);

      if (response.totp_enabled) {
        setStep('complete');
      }
    } catch (error) {
      console.error('Error checking MFA status:', error);
    }
  };

  const setupMFA = async () => {
    setIsLoading(true);
    try {
      const response = await mfaAPI.setup(userId, userEmail);
      if (response.success) {
        setQrCodeUrl(`/api/mfa/qr-code/${userId}?t=${Date.now()}`);
        setStep('verify');
        toast.success('MFA setup initiated. Please scan the QR code.');
      } else {
        toast.error(response.message || 'Failed to setup MFA');
      }
    } catch (error) {
      toast.error('Failed to setup MFA');
    } finally {
      setIsLoading(false);
    }
  };

  const verifyMFA = async () => {
    if (!verificationToken) {
      toast.error('Please enter the verification code');
      return;
    }

    setIsLoading(true);
    try {
      const response = await mfaAPI.verifySetup(userId, verificationToken);
      if (response.success) {
        setStep('complete');
        toast.success('MFA setup completed successfully!');
        onComplete && onComplete();
      } else {
        toast.error(response.message || 'Invalid verification code');
      }
    } catch (error) {
      toast.error('Failed to verify MFA setup');
    } finally {
      setIsLoading(false);
    }
  };

  const renderSetupStep = () => (
    <div className="text-center space-y-6">
      <div className="flex justify-center">
        <div className="p-4 bg-blue-100 rounded-full">
          <Shield className="h-12 w-12 text-blue-600" />
        </div>
      </div>

      <div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          Enable Multi-Factor Authentication
        </h3>
        <p className="text-gray-600">
          Add an extra layer of security to your account with MFA
        </p>
      </div>

      <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
        <div className="flex">
          <AlertTriangle className="h-5 w-5 text-yellow-400" />
          <div className="ml-3">
            <h4 className="text-sm font-medium text-yellow-800">
              Security Notice
            </h4>
            <p className="mt-1 text-sm text-yellow-700">
              MFA will be required for all future logins. Make sure you have access to your authenticator app.
            </p>
          </div>
        </div>
      </div>

      <button
        onClick={setupMFA}
        disabled={isLoading}
        className="w-full bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium disabled:opacity-50"
      >
        {isLoading ? 'Setting up...' : 'Enable MFA'}
      </button>
    </div>
  );

  const renderVerifyStep = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          Scan QR Code
        </h3>
        <p className="text-gray-600">
          Use your authenticator app to scan this QR code
        </p>
      </div>

      {qrCodeUrl && (
        <div className="flex justify-center">
          <div className="p-4 bg-white border-2 border-gray-200 rounded-lg">
            <img
              src={qrCodeUrl}
              alt="MFA QR Code"
              className="w-48 h-48"
              onError={() => toast.error('Failed to load QR code')}
            />
          </div>
        </div>
      )}

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Enter Verification Code
          </label>
          <input
            type="text"
            value={verificationToken}
            onChange={(e) => setVerificationToken(e.target.value)}
            placeholder="000000"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-center text-lg tracking-widest"
            maxLength={6}
          />
        </div>

        <div className="flex space-x-3">
          <button
            onClick={() => setStep('setup')}
            className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
          >
            Back
          </button>
          <button
            onClick={verifyMFA}
            disabled={isLoading || !verificationToken}
            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md disabled:opacity-50"
          >
            {isLoading ? 'Verifying...' : 'Verify & Complete'}
          </button>
        </div>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
        <div className="flex">
          <Smartphone className="h-5 w-5 text-blue-400" />
          <div className="ml-3">
            <h4 className="text-sm font-medium text-blue-800">
              Don't have an authenticator app?
            </h4>
            <p className="mt-1 text-sm text-blue-700">
              We recommend Google Authenticator, Authy, or Microsoft Authenticator.
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderCompleteStep = () => (
    <div className="text-center space-y-6">
      <div className="flex justify-center">
        <div className="p-4 bg-green-100 rounded-full">
          <CheckCircle className="h-12 w-12 text-green-600" />
        </div>
      </div>

      <div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          MFA Setup Complete!
        </h3>
        <p className="text-gray-600">
          Your account is now protected with multi-factor authentication
        </p>
      </div>

      <div className="bg-green-50 border border-green-200 rounded-md p-4">
        <div className="flex">
          <Shield className="h-5 w-5 text-green-400" />
          <div className="ml-3">
            <h4 className="text-sm font-medium text-green-800">
              Security Enhanced
            </h4>
            <p className="mt-1 text-sm text-green-700">
              Your account now requires both your password and a verification code to sign in.
            </p>
          </div>
        </div>
      </div>

      <button
        onClick={() => onComplete && onComplete()}
        className="w-full bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium"
      >
        Continue to Dashboard
      </button>
    </div>
  );

  if (mfaStatus?.totp_enabled) {
    return renderCompleteStep();
  }

  return (
    <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-6">
      {step === 'setup' && renderSetupStep()}
      {step === 'verify' && renderVerifyStep()}
      {step === 'complete' && renderCompleteStep()}
    </div>
  );
};

export default MFASetup;




