import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

import 'config/app_colors.dart';
import 'data/alert_repository.dart';
import 'data/firebase_alert_service.dart';
import 'screens/login_screen.dart';
import 'screens/main_screen.dart';
import 'services/authentication_service.dart';

class BlueAlertApp extends StatefulWidget {
  const BlueAlertApp({super.key});

  @override
  State<BlueAlertApp> createState() {
    return _BlueAlertAppState();
  }
}

class _BlueAlertAppState extends State<BlueAlertApp> {
  //give this variable a value later, before using it.
  late final AuthenticationService authenticationService;  // login, logout

  late final AlertRepository alertRepository;  //connect user with interface with firebase

  late final Stream<User?> authenticationStream; // real time changing 
//The stream can return two values:
// null means no user is logged in.
// A User object means a user is logged in.

  @override
  void initState() {
    super.initState();

    authenticationService = AuthenticationService();

    authenticationStream = authenticationService.authStateChanges;

    final FirebaseAlertService firebaseAlertService = FirebaseAlertService();

    alertRepository = AlertRepository(firebaseAlertService);
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'BlueAlert',
      theme: ThemeData(
        useMaterial3: true,
        scaffoldBackgroundColor: AppColors.background,
        colorScheme: ColorScheme.fromSeed(
          seedColor: AppColors.primary,
          brightness: Brightness.light,
        ).copyWith(
          primary: AppColors.primary,
          secondary: AppColors.accent,
          surface: AppColors.surface,
          error: AppColors.danger,
          outline: AppColors.border,
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: AppColors.surface,
          foregroundColor: AppColors.textPrimary,
          elevation: 0,
          surfaceTintColor: Colors.transparent,
        ),
        navigationBarTheme: const NavigationBarThemeData(
          backgroundColor: AppColors.surface,
          indicatorColor: AppColors.primarySoft,
          elevation: 6,
          shadowColor: Color(0x1A1E3A8A),
        ),
        inputDecorationTheme: const InputDecorationTheme(
          filled: true,
          fillColor: AppColors.surface,
          labelStyle: TextStyle(color: AppColors.textSecondary),
          prefixIconColor: AppColors.primary,
          enabledBorder: OutlineInputBorder(
            borderSide: BorderSide(color: AppColors.border),
            borderRadius: BorderRadius.all(Radius.circular(12)),
          ),
          focusedBorder: OutlineInputBorder(
            borderSide: BorderSide(color: AppColors.primary, width: 1.5),
            borderRadius: BorderRadius.all(Radius.circular(12)),
          ),
          errorBorder: OutlineInputBorder(
            borderSide: BorderSide(color: AppColors.danger),
            borderRadius: BorderRadius.all(Radius.circular(12)),
          ),
          focusedErrorBorder: OutlineInputBorder(
            borderSide: BorderSide(color: AppColors.danger, width: 1.5),
            borderRadius: BorderRadius.all(Radius.circular(12)),
          ),
        ),
        filledButtonTheme: FilledButtonThemeData(
          style: FilledButton.styleFrom(
            backgroundColor: AppColors.primary,
            foregroundColor: Colors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
        outlinedButtonTheme: OutlinedButtonThemeData(
          style: OutlinedButton.styleFrom(
            foregroundColor: AppColors.primaryDark,
            side: const BorderSide(color: AppColors.primary),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
        textButtonTheme: TextButtonThemeData(
          style: TextButton.styleFrom(foregroundColor: AppColors.primary),
        ),
        chipTheme: const ChipThemeData(
          backgroundColor: AppColors.primaryPale,
          side: BorderSide(color: AppColors.border),
          labelStyle: TextStyle(color: AppColors.primaryDark),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.all(Radius.circular(20)),
          ),
        ),
        snackBarTheme: const SnackBarThemeData(
          backgroundColor: AppColors.primaryDark,
          contentTextStyle: TextStyle(color: Colors.white),
          behavior: SnackBarBehavior.floating,
        ),
        dividerColor: AppColors.border,
      ),
      home: StreamBuilder<User?>(
        stream: authenticationStream,
        builder: (BuildContext context, AsyncSnapshot<User?> snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Scaffold(
              body: Center(child: CircularProgressIndicator()),
            );
          } //Firebase needs time to check the current user, so the app displays a loading indicator.

          if (snapshot.data == null) {
            return LoginScreen(authenticationService: authenticationService);
          }
          

          return MainScreen(
            alertRepository: alertRepository,
            authenticationService: authenticationService,
          );
        },
      ),
    );
  }
}
