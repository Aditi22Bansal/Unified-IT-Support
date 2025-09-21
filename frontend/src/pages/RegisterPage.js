import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Eye,
  EyeOff,
  Shield,
  CheckCircle,
  AlertTriangle,
  Lock,
  Mail,
  User,
  Phone
} from 'lucide-react';
import { authAPI } from '../services/api';
import toast from 'react-hot-toast';

const RegisterPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    fullName: '',
    password: '',
    confirmPassword: '',
    phone: '',
    role: 'customer',
    agreeToTerms: false,
    agreeToPrivacy: false
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [securityLevel, setSecurityLevel] = useState(0);
  const [errors, setErrors] = useState({});

  // Password strength requirements
  const passwordRequirements = [
    { text: 'At least 8 characters', met: formData.password.length >= 8 },
    { text: 'Contains uppercase letter', met: /[A-Z]/.test(formData.password) },
    { text: 'Contains lowercase letter', met: /[a-z]/.test(formData.password) },
    { text: 'Contains number', met: /\d/.test(formData.password) },
    { text: 'Contains special character', met: /[!@#$%^&*(),.?":{}|<>]/.test(formData.password) }
  ];

  const isPasswordStrong = passwordRequirements.every(req => req.met);
  const passwordsMatch = formData.password === formData.confirmPassword;

  // Calculate security level
  useEffect(() => {
    const level = passwordRequirements.filter(req => req.met).length;
    setSecurityLevel(level);
  }, [formData.password]);

  // Real-time validation
  useEffect(() => {
    const newErrors = {};

    // Username validation
    if (formData.username && formData.username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters';
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (formData.email && !emailRegex.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    // Phone validation
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    if (formData.phone && !phoneRegex.test(formData.phone.replace(/\s/g, ''))) {
      newErrors.phone = 'Please enter a valid phone number';
    }

    // Password validation
    if (formData.password && !isPasswordStrong) {
      newErrors.password = 'Password does not meet security requirements';
    }

    // Confirm password validation
    if (formData.confirmPassword && !passwordsMatch) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
  }, [formData, isPasswordStrong, passwordsMatch]);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleGoogleRegister = async () => {
    try {
      // In a real app, this would integrate with Google OAuth
      toast.success('Google registration would be implemented here');
    } catch (error) {
      toast.error('Google registration failed');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check for errors
    if (Object.keys(errors).length > 0) {
      toast.error('Please fix the errors before submitting');
      return;
    }

    if (!formData.agreeToTerms || !formData.agreeToPrivacy) {
      toast.error('Please agree to the terms and privacy policy');
      return;
    }

    setIsLoading(true);

    try {
      const response = await authAPI.register({
        username: formData.username,
        email: formData.email,
        fullName: formData.fullName,
        password: formData.password,
        role: formData.role
      });

      if (response.data && response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));

        toast.success('Registration successful! Welcome to IT Support Pro!');
        navigate('/dashboard');
      } else {
        throw new Error('Registration failed');
      }
    } catch (error) {
      console.error('Registration error:', error);
      toast.error('Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const getSecurityColor = () => {
    if (securityLevel <= 2) return 'text-red-500';
    if (securityLevel <= 3) return 'text-yellow-500';
    return 'text-green-500';
  };

  const getSecurityText = () => {
    if (securityLevel <= 2) return 'Weak';
    if (securityLevel <= 3) return 'Medium';
    return 'Strong';
  };

  const isFormValid = () => {
    return Object.keys(errors).length === 0 &&
           formData.username &&
           formData.email &&
           formData.fullName &&
           formData.password &&
           formData.confirmPassword &&
           isPasswordStrong &&
           passwordsMatch &&
           formData.agreeToTerms &&
           formData.agreeToPrivacy;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="flex justify-center">
            <Shield className="h-12 w-12 text-blue-600" />
          </div>
          <h2 className="mt-6 text-3xl font-bold text-gray-900">
            Create Your Account
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Join IT Support Pro and start managing your IT operations
          </p>
        </div>

        {/* Registration Form */}
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            {/* Full Name */}
            <div>
              <label htmlFor="fullName" className="block text-sm font-medium text-gray-700">
                Full Name *
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <User className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="fullName"
                  name="fullName"
                  type="text"
                  required
                  value={formData.fullName}
                  onChange={handleInputChange}
                  className={`appearance-none rounded-md relative block w-full pl-10 pr-3 py-2 border ${
                    errors.fullName ? 'border-red-300' : 'border-gray-300'
                  } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm`}
                  placeholder="Enter your full name"
                />
              </div>
              {errors.fullName && (
                <p className="mt-1 text-sm text-red-600">{errors.fullName}</p>
              )}
            </div>

            {/* Username */}
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700">
                Username *
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <User className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="username"
                  name="username"
                  type="text"
                  required
                  value={formData.username}
                  onChange={handleInputChange}
                  className={`appearance-none rounded-md relative block w-full pl-10 pr-3 py-2 border ${
                    errors.username ? 'border-red-300' : 'border-gray-300'
                  } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm`}
                  placeholder="Choose a username"
                />
              </div>
              {errors.username && (
                <p className="mt-1 text-sm text-red-600">{errors.username}</p>
              )}
            </div>

            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email Address *
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="email"
                  name="email"
                  type="email"
                  required
                  value={formData.email}
                  onChange={handleInputChange}
                  className={`appearance-none rounded-md relative block w-full pl-10 pr-3 py-2 border ${
                    errors.email ? 'border-red-300' : 'border-gray-300'
                  } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm`}
                  placeholder="Enter your email address"
                />
              </div>
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email}</p>
              )}
            </div>

            {/* Phone */}
            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
                Phone Number
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Phone className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="phone"
                  name="phone"
                  type="tel"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className={`appearance-none rounded-md relative block w-full pl-10 pr-3 py-2 border ${
                    errors.phone ? 'border-red-300' : 'border-gray-300'
                  } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm`}
                  placeholder="Enter your phone number"
                />
              </div>
              {errors.phone && (
                <p className="mt-1 text-sm text-red-600">{errors.phone}</p>
              )}
            </div>

            {/* Role Selection */}
            <div>
              <label htmlFor="role" className="block text-sm font-medium text-gray-700">
                Account Type *
              </label>
              <select
                id="role"
                name="role"
                value={formData.role}
                onChange={handleInputChange}
                className="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
              >
                <option value="customer">Customer</option>
                <option value="agent">Support Agent</option>
                <option value="admin">Administrator</option>
              </select>
            </div>

            {/* Password */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password *
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={formData.password}
                  onChange={handleInputChange}
                  className={`appearance-none rounded-md relative block w-full pl-10 pr-10 py-2 border ${
                    errors.password ? 'border-red-300' : 'border-gray-300'
                  } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm`}
                  placeholder="Create a strong password"
                />
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="text-gray-400 hover:text-gray-500 focus:outline-none"
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5" />
                    ) : (
                      <Eye className="h-5 w-5" />
                    )}
                  </button>
                </div>
              </div>

              {/* Password Requirements */}
              <div className="mt-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Password Strength:</span>
                  <span className={`font-medium ${getSecurityColor()}`}>
                    {getSecurityText()}
                  </span>
                </div>
                <div className="mt-1 bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-300 ${
                      securityLevel <= 2 ? 'bg-red-500' :
                      securityLevel <= 3 ? 'bg-yellow-500' : 'bg-green-500'
                    }`}
                    style={{ width: `${(securityLevel / 5) * 100}%` }}
                  />
                </div>
                <div className="mt-2 space-y-1">
                  {passwordRequirements.map((req, index) => (
                    <div key={index} className="flex items-center text-sm">
                      {req.met ? (
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                      ) : (
                        <div className="h-4 w-4 border border-gray-300 rounded-full mr-2" />
                      )}
                      <span className={req.met ? 'text-green-700' : 'text-gray-500'}>
                        {req.text}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Confirm Password */}
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                Confirm Password *
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  required
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  className={`appearance-none rounded-md relative block w-full pl-10 pr-10 py-2 border ${
                    errors.confirmPassword ? 'border-red-300' : 'border-gray-300'
                  } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm`}
                  placeholder="Confirm your password"
                />
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="text-gray-400 hover:text-gray-500 focus:outline-none"
                  >
                    {showConfirmPassword ? (
                      <EyeOff className="h-5 w-5" />
                    ) : (
                      <Eye className="h-5 w-5" />
                    )}
                  </button>
                </div>
              </div>
              {errors.confirmPassword && (
                <p className="mt-1 text-sm text-red-600">{errors.confirmPassword}</p>
              )}
              {formData.confirmPassword && passwordsMatch && (
                <p className="mt-1 text-sm text-green-600 flex items-center">
                  <CheckCircle className="h-4 w-4 mr-1" />
                  Passwords match
                </p>
              )}
            </div>

            {/* Terms and Privacy */}
            <div className="space-y-3">
              <div className="flex items-start">
                <input
                  id="agreeToTerms"
                  name="agreeToTerms"
                  type="checkbox"
                  checked={formData.agreeToTerms}
                  onChange={handleInputChange}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded mt-1"
                />
                <label htmlFor="agreeToTerms" className="ml-2 block text-sm text-gray-900">
                  I agree to the{' '}
                  <a href="#" className="text-blue-600 hover:text-blue-500">
                    Terms of Service
                  </a>
                </label>
              </div>
              <div className="flex items-start">
                <input
                  id="agreeToPrivacy"
                  name="agreeToPrivacy"
                  type="checkbox"
                  checked={formData.agreeToPrivacy}
                  onChange={handleInputChange}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded mt-1"
                />
                <label htmlFor="agreeToPrivacy" className="ml-2 block text-sm text-gray-900">
                  I agree to the{' '}
                  <a href="#" className="text-blue-600 hover:text-blue-500">
                    Privacy Policy
                  </a>
                </label>
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <div>
            <button
              type="submit"
              disabled={!isFormValid() || isLoading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Creating account...
                </div>
              ) : (
                'Create Account'
              )}
            </button>
          </div>

          {/* Divider */}
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-gray-50 text-gray-500">Or continue with</span>
            </div>
          </div>

          {/* Google Register */}
          <div>
            <button
              type="button"
              onClick={handleGoogleRegister}
              className="w-full flex justify-center items-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
            >
              <svg className="h-5 w-5 mr-2" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              Sign up with Google
            </button>
          </div>

          {/* Security Notice */}
          <div className="bg-green-50 border border-green-200 rounded-md p-4">
            <div className="flex">
              <Shield className="h-5 w-5 text-green-400" />
              <div className="ml-3">
                <h3 className="text-sm font-medium text-green-800">
                  Your Security is Our Priority
                </h3>
                <ul className="mt-1 text-sm text-green-700 space-y-1">
                  <li>• All data encrypted in transit and at rest</li>
                  <li>• Multi-factor authentication available</li>
                  <li>• Regular security audits and updates</li>
                  <li>• GDPR and SOC 2 compliant</li>
                </ul>
              </div>
            </div>
          </div>
        </form>

        {/* Sign In Link */}
        <div className="text-center">
          <p className="text-sm text-gray-600">
            Already have an account?{' '}
            <Link to="/login" className="font-medium text-blue-600 hover:text-blue-500">
              Sign in here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
