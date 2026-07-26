import 'package:firebase_auth/firebase_auth.dart';

import '../exceptions/app_auth_exception.dart';

class AuthenticationService {
  AuthenticationService({FirebaseAuth? firebaseAuth})
    : _firebaseAuth = firebaseAuth ?? FirebaseAuth.instance;

  final FirebaseAuth _firebaseAuth;

  Stream<User?> get authStateChanges {
    return _firebaseAuth.authStateChanges();
  } // maintaining the screen such as login if user null and main page if user exit 

  User? get currentUser {
    return _firebaseAuth.currentUser;
  } // check who is current login 

  Future<void> login({required String email, required String password}) async {
    final String cleanedEmail = email.trim().toLowerCase();

    if (cleanedEmail.isEmpty) {
      throw const AppAuthException('Please enter your email.');
    }

    if (password.isEmpty) {
      throw const AppAuthException('Please enter your password.');
    }

    try {
      await _firebaseAuth.signInWithEmailAndPassword(
        email: cleanedEmail,
        password: password,
      );
    } on FirebaseAuthException catch (error) {
      throw AppAuthException(_getLoginErrorMessage(error.code));
    } catch (_) {
      throw const AppAuthException('Login failed. Please try again.');
    }
  }

  Future<void> sendPasswordReset({required String email}) async {
    final String cleanedEmail = email.trim().toLowerCase();

    if (cleanedEmail.isEmpty) {
      throw const AppAuthException(
        'Enter your Gmail before clicking Forgot password.',
      );
    }

    if (!cleanedEmail.endsWith('@gmail.com')) {
      throw const AppAuthException('Email must end with @gmail.com.');
    }

    try {
      await _firebaseAuth.sendPasswordResetEmail(email: cleanedEmail);
    } on FirebaseAuthException catch (error) {
      throw AppAuthException(_getResetErrorMessage(error.code));
    } catch (_) {
      throw const AppAuthException('Could not send the reset email.');
    }
  }

  Future<void> logout() async {
    await _firebaseAuth.signOut();
  }

  String _getLoginErrorMessage(String code) {
    switch (code) {
      case 'invalid-email':
        return 'The email address is invalid.';

      case 'invalid-credential':
      case 'wrong-password':
      case 'user-not-found':
        return 'Incorrect email or password.';

      case 'user-disabled':
        return 'This account has been disabled.';

      case 'too-many-requests':
        return 'Too many attempts. Try again later.';

      case 'network-request-failed':
        return 'Check your internet connection.';

      case 'operation-not-allowed':
        return 'Email/password authentication is not enabled.';

      default:
        return 'Login failed: $code';
    }
  }

  String _getResetErrorMessage(String code) {
    switch (code) {
      case 'invalid-email':
        return 'The email address is invalid.';

      case 'user-not-found':
        return 'No BlueAlert account exists with this email.';

      case 'too-many-requests':
        return 'Too many reset requests. Try again later.';

      case 'network-request-failed':
        return 'Check your internet connection.';

      case 'operation-not-allowed':
        return 'Email/password authentication is not enabled.';

      default:
        return 'Password reset failed: $code';
    }
  }
}
