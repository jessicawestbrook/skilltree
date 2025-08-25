-- Add subcategories to Multivariable Calculus
-- Parent ID: 803a7324-fb28-4848-9ca5-7f79c28a3175

-- Core Concepts
INSERT INTO skill_tree_nodes (id, name, parent_id) VALUES
  (gen_random_uuid(), 'Vectors and Vector Operations', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Parametric Equations and Curves', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Polar Coordinates', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Functions of Several Variables', '803a7324-fb28-4848-9ca5-7f79c28a3175');

-- Differentiation
INSERT INTO skill_tree_nodes (id, name, parent_id) VALUES
  (gen_random_uuid(), 'Partial Derivatives', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Directional Derivatives and Gradients', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Chain Rule for Multiple Variables', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Tangent Planes and Linear Approximation', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Optimization and Lagrange Multipliers', '803a7324-fb28-4848-9ca5-7f79c28a3175');

-- Integration
INSERT INTO skill_tree_nodes (id, name, parent_id) VALUES
  (gen_random_uuid(), 'Double Integrals', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Triple Integrals', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Change of Variables and Jacobians', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Cylindrical and Spherical Coordinates', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Applications of Multiple Integrals', '803a7324-fb28-4848-9ca5-7f79c28a3175');

-- Vector Calculus
INSERT INTO skill_tree_nodes (id, name, parent_id) VALUES
  (gen_random_uuid(), 'Vector Fields', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Line Integrals', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Surface Integrals', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Green''s Theorem', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Stokes'' Theorem', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Divergence Theorem', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Curl and Divergence', '803a7324-fb28-4848-9ca5-7f79c28a3175');

-- Advanced Topics
INSERT INTO skill_tree_nodes (id, name, parent_id) VALUES
  (gen_random_uuid(), 'Differential Forms', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Implicit Function Theorem', '803a7324-fb28-4848-9ca5-7f79c28a3175'),
  (gen_random_uuid(), 'Taylor Series in Multiple Variables', '803a7324-fb28-4848-9ca5-7f79c28a3175');